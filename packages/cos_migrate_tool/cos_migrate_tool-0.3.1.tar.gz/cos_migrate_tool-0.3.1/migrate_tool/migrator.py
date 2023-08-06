# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from os import path
from logging import getLogger
from logging import getLogger, basicConfig, DEBUG
from sys import stderr
import time
from threading import Timer, Thread

from migrate_tool.worker import Worker
from migrate_tool.filter import Filter

logger = getLogger(__name__)


class BaseMigrator(object):

    def start(self):
        pass

    def stop(self):
        pass

    @property
    def status(self):
        """ Query migrate status

        :return: dict like {'success': 213, 'failure': 19, 'state': 'running'}
        """
        pass


class ThreadMigrator(BaseMigrator):
    """migrator Class, consisted of:
        1. Workers
        2. InputStorageService
        3. OutputStorageService
        4. Filter: Determines whether the file has been moved

    """

    def __init__(self, input_service, output_service, work_dir=None, threads=10, record_succ=True, *args, **kwargs):

        self._input_service = input_service
        self._output_service = output_service
        self._record_succ = record_succ

        self._work_dir = work_dir or os.getcwd()
        self._filter = Filter(self._work_dir, record_succ)

        self._worker = Worker(work_dir=self._work_dir,
                              file_filter=self._filter,
                              input_service=self._input_service,
                              output_service=self._output_service,
                              threads_num=threads)

        self._stop = False
        self._finish = False
        self._threads = []

        # if path.exists(path.join(self._work_dir, 'filter.json')):
        #    with open(path.join(self._work_dir, 'filter.json'), 'r') as f:
        #       self._filter.loads(f.read())
        #        logger.info("loads bloom filter snapshot successfully.")

    def log_status_thread(self):
        while not self._stop:
            logger.info("working, {} tasks successfully, {} tasks failed.".format(self._worker.success_num,
                                                                                  self._worker.failure_num))
            time.sleep(3)

    def work_thread(self):
        assert self._output_service is not None
        marker = self._filter.get_marker() #if record_succ is true,always return empty
        try:
            for task in self._output_service.list(marker):

                if self._stop:
                    logger.info('stop list,break...')
                    break

                # print type(task)
                object_name_ = task.key
                if isinstance(object_name_, unicode):
                    object_name_ = object_name_.encode('utf-8')

                if self._filter.query(object_name_):
                    # object had been migrated
                    logger.info("{} has been migrated, skip it".format(object_name_))

                else:
                    # not migrated
                    self._filter.add_doing_task(object_name_)
                    self._worker.add_task(task)
                    self._filter.set_marker(object_name_)
                    logger.info("{} has been submitted, waiting for migrating".format(object_name_))
            else:
                self._finish = True
        except Exception as e:
            self._finish = True
            logger.exception(str(e))

    def start(self):
        log_status_thread = Thread(target=self.log_status_thread, name='log_status_thread')
        log_status_thread.daemon = True
        self._threads.append(log_status_thread)

        work_thread = Thread(target=self.work_thread, name='work_thread')
        work_thread.daemon = True
        self._threads.append(work_thread)

        for t in self._threads:
            t.start()

        self._worker.start()

    def stop(self, force=False):
        if force:
            self._worker.term()
        else:
            self._worker.stop()

        self._stop = True

        for t in self._threads:
            t.join()

    def status(self):
        return {'success': self._worker.success_num, 'fail': self._worker.failure_num, 'finish': self._finish}

if __name__ == '__main__':
    from migrate_tool.services.LocalFileSystem import LocalFileSystem

    migrator = ThreadMigrator(input_service=LocalFileSystem(workspace='F:\\Workspace\\tmp'),
                              output_service=LocalFileSystem(workspace='F:\\logstash-conf'))
    migrator.start()

    import time
    time.sleep(10)
    migrator.stop()
