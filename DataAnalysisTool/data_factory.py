'''
Created on Oct 18, 2016

@author: Carlos Garcia - carlos@carlosgarcia.co
'''
# Internal Imports
import csv_handle
import python_handle


class DataFactory(object):
    '''
    This is a factory class base on pattern, this factory will select the
    correct class to have data operations
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._class_list = {'.csv': csv_handle.CSVHandle,
                            '.py': python_handle.PythonHandle}

    def get_class(self, data_type):
        '''
        It return the class that was found to handle the data
        :param data_type: The type of IO/data requested
        '''
        return self._class_list[data_type]
