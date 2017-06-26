'''
Created on Oct 18, 2016

@author: Carlos Garcia - carlos@carlosgarcia.co
'''
from abc import ABCMeta, abstractmethod


class DataInterface:
    '''
    This interface class it force the IO classes to have at least this methods
    to communicate with the main class
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_file(self, path):
        '''
        It reads a file
        :param file_path: The path where the file is in the system
        :type file_path: str
        '''
        pass

    @abstractmethod
    def write_file(self, path, content):
        '''
        It writes a file
        :param path: The path where the file is going to be save
        :type path: str
        '''
        pass
