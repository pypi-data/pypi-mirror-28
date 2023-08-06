# -*- coding: utf8 -*-
import json
import logging

import copy

from ..backend_mixin import BackendMixin
from .base_metadata_db import BaseMetadataDB, MetadataOperationError
from six.moves.urllib.parse import urlencode


class BackendMetadataDB(BackendMixin, BaseMetadataDB):
    def __init__(self, connection, config, handle_api):
        super(BackendMetadataDB, self).__init__(connection, config, handle_api)

    def _create_table(self):
        pass

    def _query_head_data(self, sha_list):
        with self._connection.get_cursor() as session:
            url = 'data_volumes/%s/metadata/head' % self._volume_id
            msg = {
                'sha': sha_list,
            }

            result = self._handle_api(self._config, session.post, url, msg)

            for data_item in result.get('metadata_json') or []:
                yield json.loads(data_item)

    def _add_missing_columns(self, data_object):
        pass

    def get_data_for_commit(self, sha, commit_sha):
        raise NotImplementedError(self.get_data_for_commit)

    def _add_data(self, data):
        pass

    def add_data(self, data):
        if not data:
            logging.debug('no data provided')
            return

        logging.debug('add data %s', data)

        with self._connection.get_cursor() as session:
            url = 'data_volumes/%s/metadata/head/add' % self._volume_id

            msg = {
                'metadata_url': data,
            }

            return self._handle_api(self._config, session.post, url, msg)

    def query(self, query_text, max_results, start_index):
        def _iter_data():
            for data_point in result.get('data_points') or []:
                result_data_point = {}

                for key, val in data_point.items():
                    if key == 'meta':
                        meta = result_data_point.setdefault('meta', {})
                        for meta_key_val in data_point['meta']:
                            meta[meta_key_val['key']] = meta_key_val.get('val')
                    else:
                        result_data_point[key] = val

                yield result_data_point

        with self._connection.get_cursor() as session:
            version_query = query_text if query_text else '@version:head'

            params = {
                'query': version_query
            }

            if max_results:
                params['max_results'] = max_results

            if start_index:
                params['start_index'] = start_index

            url = 'data_volumes/%s/query/?%s' % (self._volume_id, urlencode(params))

            result = self._handle_api(self._config, session.get, url)

            if not result['ok']:
                raise MetadataOperationError(result['error'])

            return _iter_data(), int(result.get('total_data_points', 0))

    def _query(self, sql_vars, select_fields, where, max_results, start_index):
        raise NotImplementedError(self._query)

    def get_all_data(self, sha):
        raise NotImplementedError(self.get_all_data)

    def end_commit(self):
        raise NotImplementedError(self.end_commit)

    def begin_commit(self, commit_sha, tree_id):
        raise NotImplementedError(self.begin_commit)
