# -*- coding:utf-8 -*-
from Queue import Queue, Empty
from threading import Thread
from os import path, makedirs
from logging import getLogger
from threading import Lock

logger = getLogger(__name__)
fail_logger = getLogger('migrate_tool.fail_file')


class Worker(object):
    def __init__(self, work_dir, file_filter, input_service, output_service, threads_num=5, max_size=30):
        self._input_service = input_service
        self._output_service = output_service
        self._filter = file_filter
        self._work_dir = work_dir

        self._threads_num = threads_num
        self._threads_pool = []
        self._queue = Queue(maxsize=max_size)
        self._stop = False
        self._succ = 0
        self._fail = 0
        self._lock = Lock()

    def __work_thread(self):

        while not self._stop:
            # logger.info("worker stop: " + str(self._stop))
            try:
                # logger.debug("try to get task")
                task = self._queue.get_nowait()
                # logger.debug("get task succeefully")
                self._queue.task_done()
            except Empty:
                logger.debug("Empty queue" + str(self._stop))
                if self._stop:
                    break
                else:
                    import time
                    time.sleep(1)
                    continue
            
            task_path = task.key
            
            if task_path.startswith('/'):
                task_path = task_path[1:]

            if isinstance(task_path, str):
                task_path = task_path.decode('utf-8')

            import uuid
            localpath = unicode(path.join(self._work_dir, uuid.uuid1().hex))

            if task.size is None:
                logger.warn("{file_path} task doesn't contains size attribute".format(
                    file_path=task_path.encode('utf-8')
                ))
                self._fail += 1
                fail_logger.error(task_path)
                continue

            try:
                try:
                    makedirs(path.dirname(localpath))
                except OSError as e:
                    # directory is exists
                    logger.debug(str(e))

                try:
                    ret = self._input_service.exists(task)
                    if ret:
                        logger.info("{file_path} exists".format(file_path=task_path.encode('utf-8')))
                        with self._lock:
                            self._succ += 1
                            self._filter.add(task_path)
                        continue
                except Exception as e:
                    logger.exception("exists failed")

                try:
                    self._output_service.download(task, localpath)
                except Exception as e:
                    logger.exception("download failed")
                    self._fail += 1
                    fail_logger.error(task_path)
                    continue

                try:
                    self._input_service.upload(task, localpath)
                except Exception:
                    logger.exception("upload {} failed".format(task_path.encode('utf-8')))
                    self._fail += 1
                    fail_logger.error(task_path)
                    continue

                try:
                    import os
                    if isinstance(localpath, unicode):
                        localpath = localpath.encode('utf-8')

                    os.remove(localpath)
                    try:
                        os.removedirs(path.dirname(localpath))
                    except OSError:
                        pass
                except Exception as e:
                    logger.exception(str(e))
                    continue

                try:
                    ret = self._input_service.exists(task)
                    if ret:
                        if isinstance(task_path, unicode):
                            logger.info("inc succ with {}".format(task_path.encode('utf-8')))
                        else:
                            logger.info("inc succ with {}".format(task_path.encode('utf-8')))

                        with self._lock:
                            self._succ += 1
                            self._filter.add(task_path)
                        continue
                    else :
                        logger.exception("there is not expected object in service, you need to re-run this application again")
                
                except Exception as e:
                    logger.exception("exists failed")

            except Exception:
                logger.exception("try except for deleting file")

            finally:
                self._filter.del_doing_task(task_path)
                import os
                if isinstance(localpath, unicode):
                    localpath = localpath.encode('utf-8')

                try:
                    os.remove(localpath)
                    os.removedirs(path.dirname(localpath))
                except OSError:
                    pass

    def add_task(self, task):
        # blocking
        self._queue.put(task)

    def start(self):
        self._threads_pool = [Thread(target=self.__work_thread) for _ in range(self._threads_num)]
        for t in self._threads_pool:
            t.start()

    def stop(self):

        self._queue.join()
        self.term()

    def term(self):
        self._stop = True
        logger.info("try to stop migrate process.")
        # while any([t.is_alive() for t in self._threads_pool]):
        #     map(lambda i: i.join(5), filter(lambda j: j.is_alive(), self._threads_pool))
        #     print filter(lambda j: j.is_alive(), self._threads_pool)

        map(lambda i: i.join(), self._threads_pool)

    @property
    def success_num(self):
        return self._succ

    @property
    def failure_num(self):
        return self._fail
