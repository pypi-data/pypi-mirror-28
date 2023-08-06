# -*- coding: utf8 -*-
import glob
import os
import shutil
import errno

import re
import six

ignore_files = ['.DS_Store']


def enumerate_path(path):
    path = expend_and_validate_path(path)
    if is_glob(path):
        for path in glob.glob(path):
            yield path

        return

    if os.path.isfile(path):
        yield path
        return

    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, followlinks=True):
            for file_ in files:
                if file_ in ignore_files:
                    continue

                yield os.path.join(root, file_)


def enumerate_paths(paths):
    if isinstance(paths, six.string_types):
        paths = [paths]

    for path in paths:
        path = path.rstrip('\n')
        for file_ in enumerate_path(path):
            yield file_


def get_total_files_in_path(paths, callback=None):
    total_files = 0

    for file_name in enumerate_paths(paths):
        count_file = True
        if callback is not None:
            count_file = callback(file_name)

        if count_file:
            total_files += 1

    return total_files


def is_glob(path):
    return '*' in path or '?' in path


def has_var(path):
    return '$' in path


def expend_and_validate_path(path, expand_vars=True, validate_path=True, abs_path=True):
    if path is None:
        return path

    result_path = os.path.expanduser(path)

    if expand_vars:
        result_path = os.path.expandvars(result_path)

    if abs_path:
        result_path = os.path.abspath(result_path)

    if not is_glob(result_path) and validate_path and not os.path.exists(result_path):
        raise IOError()

    if path.endswith(os.sep):
        result_path = os.path.join(result_path, '')

    return result_path


def get_batch_of_files_from_paths(paths, batch_size):
    batch = []
    for file_or_path in enumerate_paths(paths):
        batch.append(file_or_path)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if len(batch) > 0:
        yield batch


def safe_make_dirs(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise


def path_elements(path):
    if path.endswith(os.sep):
        path = path[:-1]

    folders = []
    while True:
        path, folder = os.path.split(path)

        if len(folder) > 0:
            folders.append(folder)
            continue

        if len(path) > 0:
            folders.append(path)

        break

    folders.reverse()

    return folders


def safe_rm_tree(path):
    try:
        shutil.rmtree(path)
    except OSError as ex:
        if ex.errno != errno.ENOENT:
            raise


class DestPathEnum(object):
    @classmethod
    def find_root(cls, dest):
        elements = path_elements(dest)

        root = []
        for element in elements:
            if has_var(element):
                break

            root.append(element)

        return os.path.join(*root)

    @classmethod
    def get_path_vars(cls, pattern, path):
        if path is None:
            return {}

        path_no_ext, file_extension = os.path.splitext(path)

        # in case the user has already specify '.' in the ext don't use dot in the var
        if '.$ext' in pattern or '.$@ext' in pattern:
            file_extension = file_extension[1:]

        return {
            'name': os.path.basename(path),
            'dir': os.path.dirname(path),
            'base_name': os.path.basename(path_no_ext),
            'ext': file_extension,
            'extension': file_extension
        }

    @classmethod
    def ___add_sys_var(cls, name, value, current_vars):
        current_vars['@' + name] = value

        if name not in current_vars:
            current_vars[name] = value

    @classmethod
    def __fill_in_vars(cls, path, replace_vars):
        replace_vars_keys = sorted(replace_vars.keys(), reverse=True)

        for var_name in replace_vars_keys:
            var_value = replace_vars[var_name]
            path = path.replace('$' + var_name, str(var_value))
            path = path.replace('#' + var_name, str(var_value))

        return path

    @classmethod
    def get_full_path(cls, dest, item):
        for key, val in cls.get_path_vars(dest, item.get('@path')).items():
            cls.___add_sys_var(key, val, item)

        phase = item.get('@phase')
        cls.___add_sys_var('phase', phase, item)
        item['@'] = phase

        dest_file = cls.__fill_in_vars(dest, item)

        return dest_file

    @classmethod
    def get_dest_path(cls, dest_folder, dest_file):
        if not dest_file:
            dest_file = '$@name'

        return os.path.join(dest_folder, dest_file)


def create_dir(dirname):
    if not dirname or os.path.exists(dirname):
        return

    try:
        os.makedirs(dirname)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


def remove_dir(dirname):
    try:
        shutil.rmtree(dirname)
    except (OSError, IOError):
        pass


def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))


def flatten_dir(root_dir):
    root_walk = os.walk(root_dir)
    _, top_level_dirs, _ = next(root_walk)

    for dirpath, _, filenames in root_walk:
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            shutil.move(filepath, root_dir)

    for top_level_dir in top_level_dirs:
        remove_dir(os.path.join(root_dir, top_level_dir))


def remove_moniker(name):
    try:
        index = name.index('://')
        return name[index + 3:]
    except ValueError:
        return name
