# -*- coding: utf8 -*-
import json
import logging
import tempfile
from contextlib import closing
import sys
import os
from uuid import uuid4
import datetime
import click
import requests
from six import wraps
from tqdm import tqdm
from mali_commands.config import Config
from mali_commands.data_volume import with_repo
from mali_commands.json_utils import multi_line_json_from_data, normalize_item
from mali_commands.legit import MetadataOperationError
from mali_commands.legit.dulwich import porcelain
from mali_commands.legit.dulwich.index import index_entry_from_stat
from mali_commands.legit.dulwich.repo import blob_from_path_and_stat
from mali_commands.legit.multi_process_control import get_multi_process_control
from mali_commands.path_utils import enumerate_paths, get_batch_of_files_from_paths, safe_make_dirs, DestPathEnum
from mali_commands.utils import PrintStatus


def wrap_exceptions(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        from botocore.exceptions import NoCredentialsError

        try:
            return fn(*args, **kwargs)
        except NoCredentialsError as ex:
            click.echo('S3/boto', err=True)
            click.echo(ex.message, err=True)
            exit(1)

    return decorated


def _download_entity(config_init_dict, volume_id, dest_file, item_id, item_meta):
    DataSync.download_entity(config_init_dict, volume_id, dest_file, item_id, item_meta)


class DataSync(object):
    def __init__(self, ctx, repo, no_progressbar):
        self.__ctx = ctx
        self.__repo = repo
        self.__no_progressbar = no_progressbar

    def __upload_file_for_processing(self, file_obj, file_description):
        from mali_commands.legit.gcs_utils import do_upload

        volume_id = self.__repo.data_volume_config.volume_id

        data_object_name = '%s/temp/%s_%s.json' % (volume_id, file_description, uuid4().hex)

        url = 'data_volumes/{volume_id}/gcs_urls'.format(volume_id=volume_id)

        headers = {'Content-Type': 'application/json'}

        msg = {
            'methods': 'PUT',
            'paths': [data_object_name],
            'content_type': 'application/json',
            'temp': True,
        }

        result = self.__ctx.obj.handle_api(self.__ctx.obj, requests.post, url, msg)

        put_url = result['put'][0]

        gcs_auth = self.__repo.data_volume_config.object_store_config.get('auth')

        def update_bar(c):
            bar.update(c)

        logging.debug('uploading %s', data_object_name)
        with tqdm(total=file_obj.tell(), desc="Uploading {}".format(file_description), unit=' KB', ncols=80,
                  disable=self.__no_progressbar, unit_scale=True) as bar:
            do_upload(gcs_auth, None, data_object_name, file_obj, headers, head_url=None, put_url=put_url,
                      callback=update_bar)

        return data_object_name

    def __process_index(self, object_name):
        index = self.__repo.open_index()

        change_set = self.__process_with_status('Index', lambda: index.get_changeset(data='gs://' + object_name))

        total_modify_files = 0
        total_new_files = 0

        files_to_upload = tempfile.TemporaryFile('w+')

        for name, op in change_set:
            if op == 'm':
                total_modify_files += 1
            elif op == 'i':
                total_new_files += 1
            else:
                continue

            files_to_upload.write(os.path.join(self.__repo.data_path, name) + '\n')

        total_files_to_upload = total_modify_files + total_new_files
        files_to_upload.seek(0)

        return files_to_upload, total_files_to_upload

    @classmethod
    def __process_with_status(cls, process_type, callback):
        start_time = datetime.datetime.utcnow()
        status_line = PrintStatus()
        with closing(status_line):
            status_line.print_status('Processing %s' % process_type)
            result = callback()
            status_line.print_status('Processing %s Done (%s)' % (process_type, datetime.datetime.utcnow() - start_time))

        return result

    def upload_and_update_index(self, file_obj):
        object_name = self.__upload_file_for_processing(file_obj, 'Index')

        files_to_upload, total_files_to_upload = self.__process_index(object_name)

        return files_to_upload, total_files_to_upload

    def upload_and_update_metadata(self, file_obj):
        object_name = self.__upload_file_for_processing(file_obj, 'Metadata')

        self.__process_with_status('Metadata', lambda: self.__repo.metadata.add_data(data='gs://' + object_name))

    def create_combined_index_and_metadata(self, files):
        import humanize

        combined_meta_files = tempfile.TemporaryFile('w+')
        combined_index_files = tempfile.TemporaryFile('w+')

        total_files = 0
        total_files_size = 0
        total_metadata = 0
        status_line = PrintStatus()
        with closing(status_line):
            for file_name in enumerate_paths(files):
                rel_path = os.path.relpath(file_name, self.__repo.data_path)

                metadata_ext = '.metadata.json'
                if file_name.lower().endswith(metadata_ext):
                    data_point_file_name = file_name[:-len(metadata_ext)]

                    if not os.path.isfile(data_point_file_name):
                        continue

                    rel_path = rel_path[:-len(metadata_ext)]

                    with open(file_name) as metadata_file:
                        data = json.load(metadata_file)
                        multi_line_json_from_data({rel_path: data}, combined_meta_files)
                        total_metadata += 1
                        continue

                total_files += 1

                st = os.lstat(file_name)

                fs_encoding = sys.getfilesystemencoding()
                fs_path_bytes = file_name.encode(fs_encoding)

                blob = blob_from_path_and_stat(fs_path_bytes, st)

                ctime, mtime, dev, ino, mode, uid, gid, size, sha, flags, url = index_entry_from_stat(st, blob.id, 0)

                total_files_size += size

                status_line.print_status(
                    'Total files {:,} ({}) (metadata found: {:,})', total_files,
                    humanize.naturalsize(total_files_size), total_metadata)

                params = {
                    'ctime': ctime,
                    'mtime': mtime,
                    'size': size,
                    'sha': sha,
                    'mode': mode,
                }

                multi_line_json_from_data({rel_path: params}, combined_index_files)

            combined_meta_files.flush()
            combined_index_files.flush()

        if total_metadata == 0:
            combined_meta_files = None

        return combined_meta_files, combined_index_files

    @wrap_exceptions
    def upload_in_batches(self, paths, total_files, callback=None):
        batch_size = max(min(total_files // 100, 250), 250)  # FIXME: hardcoded

        for current_batch in get_batch_of_files_from_paths(paths, batch_size):
            porcelain.add(self.__repo, current_batch, self.__repo.data_volume_config.embedded, callback=callback)

    @classmethod
    def download_entity(cls, config_init_dict, volume_id, dest_file, item_id, item_meta):
        import google.api_core.exceptions

        config = Config(**config_init_dict)

        with with_repo(config, volume_id, read_only=True) as repo:
            try:
                _, data = repo.object_store.get_raw(item_id)
            except requests.exceptions.HTTPError as ex:
                if ex.response.status_code == 404:
                    return

                raise
            except google.api_core.exceptions.NotFound:
                return

            safe_make_dirs(os.path.dirname(dest_file))

            def append_id(filename, uid):
                name, ext = os.path.splitext(filename)
                return "{name}_{uid}{ext}".format(name=name, uid=uid, ext=ext)

            if os.path.exists(dest_file):
                dest_file = append_id(dest_file, item_id)

            json_metadata_name = dest_file + '.metadata.json'

            with open(json_metadata_name, 'w') as metadata_file:
                json.dump(item_meta, metadata_file)

            with open(dest_file, 'wb') as f:
                f.write(data)

    def download_all(self, query, root_folder, dest_pattern, batch_size, processes):
        multi_process_control = get_multi_process_control(processes)
        return self.__download_all(multi_process_control, query, root_folder, dest_pattern, batch_size)

    def __download_results(self, process_control, dest_pattern, results, callback):
        volume_id = self.__repo.data_volume_config.volume_id

        def wrap_callback_func(current_item, current_full_path):
            def wrapper(_):
                callback(current_full_path, current_item)

            return wrapper

        for item in results:
            normalized_item = normalize_item(item)
            config_init_dict = self.__ctx.obj.config.init_dict

            full_path = DestPathEnum.get_full_path(dest_pattern, normalized_item)

            process_control.execute(
                _download_entity, args=(config_init_dict, volume_id, full_path, item['id'], item.get('meta', {})),
                callback=wrap_callback_func(item, full_path))

    def __download_all(self, multi_process_control, query, root_folder, dest_pattern, batch_size):
        def get_next_results(query_index):
            current_results, current_total_data_points = self.__repo.metadata.query(
                query, max_results=batch_size, start_index=query_index)

            return list(current_results), current_total_data_points

        def handle_item(file_name, item):
            rel_path = os.path.relpath(file_name, root_folder)
            phase = item.get('phase', 'all')
            phase_meta.setdefault(phase, {})[rel_path] = item

            bar.update()

        start_index = 0

        results, total_data_points = get_next_results(start_index)

        phase_meta = {}

        with tqdm(total=total_data_points, desc="Downloading", unit=' data point', ncols=80, disable=self.__no_progressbar) as bar:
            with closing(multi_process_control):
                try:
                    while True:
                        self.__download_results(multi_process_control, dest_pattern, results, handle_item)

                        if len(results) != batch_size:
                            break

                        start_index += len(results)

                        results, _ = get_next_results(start_index)
                except MetadataOperationError as ex:
                    click.echo(ex.message, err=True)
                except KeyboardInterrupt:
                    multi_process_control.terminate()
                    multi_process_control.close()

        return phase_meta

    def save_metadata(self, root_dest, metadata):
        with tqdm(total=len(metadata), desc="saving metadata", unit=' files', ncols=80, disable=self.__no_progressbar) as bar:
            for key, val in metadata.items():
                if key is None:
                    key = 'unknown'

                json_metadata_file = os.path.join(root_dest, key + '.metadata.json')

                with open(json_metadata_file, 'w') as f:
                    json.dump(val, f)

                bar.update()
