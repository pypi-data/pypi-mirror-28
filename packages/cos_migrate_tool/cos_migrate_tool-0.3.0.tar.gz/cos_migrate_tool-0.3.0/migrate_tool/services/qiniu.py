# -*- coding: utf-8 -*-
from __future__ import absolute_import

from logging import getLogger
from migrate_tool import storage_service
from migrate_tool.task import Task
from qiniu import Auth
from qiniu import BucketManager
import requests

logger = getLogger(__name__)


class TokenException(Exception):
    pass


class QiniuStorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):

        accesskeyid = kwargs['accesskeyid']
        accesskeysecret = kwargs['accesskeysecret']
        self._bucket = kwargs['bucket']
        self._auth = Auth(accesskeyid, accesskeysecret)
        self._domain = kwargs['domain_url']
        self._qiniu_api = BucketManager(self._auth)
        self._prefix = kwargs['prefix'] if 'prefix' in kwargs else ''

    def download(self, task, local_path):
        cos_path = task.key
        if isinstance(local_path, str):
            local_path = local_path.decode('utf-8')
        if cos_path.startswith('/'):
            cos_path = cos_path[1:]

        if isinstance(cos_path, unicode):
            cos_path = cos_path.encode('utf-8')
            from urllib import quote
            cos_path = quote(cos_path)

        base_url = 'http://%s/%s' % (self._domain, cos_path)
        # print base_url
        private_url = self._auth.private_download_url(base_url, expires=3600)
        # print private_url
        logger.debug("private url: " + private_url)

        for i in range(20):
            try:
                ret = requests.get(private_url, stream=True)

                if ret.status_code != 200:
                    raise SystemError("download file from qiniu failed")

                with open(local_path.encode('utf-8'), 'wb') as fd:
                    for chunk in ret.iter_content(1024):
                        fd.write(chunk)
                if task.size is not None:
                    from os import path
                    if path.getsize(local_path.encode('utf-8')) != task.size:
                        raise IOError("Download failed error")
                    else:
                        logger.info("download successful")
                        break
            except:
                pass
        else:
            raise IOError("Download failed error")

    def upload(self, cos_path, local_path):
        raise NotImplementedError

    def list(self, marker):
        limit = 100
        delimiter = None
        marker = None

        eof = False

        while not eof:
            try:
                ret, eof, info = self._qiniu_api.list(self._bucket, self._prefix, marker, limit, delimiter)
                if ret is None:
                    logger.warn("ret is None")
                    if info.error == 'bad token':
                        raise TokenException
                    else:
                        logger.warn(info.text_body)
                        raise IOError(info.error)

                for i in ret['items']:
                    logger.info("yield new object: {}".format(i['key']))
                    yield Task(i['key'], i['fsize'], None, None)

                if eof is True:
                    logger.info("eof is {}".format(eof))
                    continue

                if not eof and 'marker' in ret:
                    marker = ret['marker']
                else:
                    eof = True
            except TokenException as e:
                eof = True
                logger.warn("Your accessid/accesskey is incorrect, Please double check your configures")
            except Exception as e:
                logger.exception("list exception: " + str(e))

    def exists(self, _path):
        raise NotImplementedError
