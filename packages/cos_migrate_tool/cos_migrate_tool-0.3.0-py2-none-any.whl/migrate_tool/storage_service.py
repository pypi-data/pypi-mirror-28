# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class StorageService(object):
    """ The abstract class for Storage Services. you must impl following functions.

    `path` is `/path/to/your/object`
    `localpath` is full local path.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def download(self, task, localpath):
        """ downloads object from service, and saves to local disk

        :param path: path on Services
        :param localpath: local path on Disk
        :return: success or failure
        """
        pass

    @abstractmethod
    def upload(self, task, localpath):
        """ uploads local file to service

        :param path: path on Service
        :param localpath: local path on Disk
        :return: success or failure
        """
        pass

    @abstractmethod
    def exists(self, task):
        """ query for existence of object

        :param task: path on Service
        :return:
        """
        pass

    @abstractmethod
    def list(self, marker):
        """
        :return: iterator for 'a/b/c.txt', 'a/b/d.txt', not starts with '/'
        """
        pass
