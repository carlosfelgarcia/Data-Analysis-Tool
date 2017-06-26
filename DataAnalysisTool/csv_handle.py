'''
Created on Oct 18, 2016

@author: Carlos Garcia - carlos@carlosgarcia.co
'''

# External Libraries Imports
import pandas as pd

# Internal Imports
from interface_data import DataInterface


class CSVHandle(DataInterface):
    '''
    This class handle all the different operations for csv files, follow the
    "DataInterface" interface.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def read_file(self, path):
        '''
        It reads the csv file with pandas library
        :param path: The path to the file
        :type path: str
        '''
        return pd.read_csv(path)

    def write_file(self, path, content):
        '''
        It writes a csv file using pandas
        :param path: The path where the file is going to be save
        :type path: str
        :param content: The content of the csv file
        :type content: pandas.DataFrame
        '''
        if isinstance(content, pd.DataFrame):
            content.to_csv(path, index=False)
