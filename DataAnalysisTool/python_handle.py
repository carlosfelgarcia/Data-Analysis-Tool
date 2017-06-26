'''
Created on Oct 18, 2016

@author: Carlos Garcia - carlos@carlosgarcia.co
'''

# Internal Imports
from interface_data import DataInterface
from shutil import copy2, move
from os import remove, path


class PythonHandle(DataInterface):
    """
    This class follow the interface convention of "DataInterface", and it
    handles all the operations for python files
    """

    def __init__(self):
        """
        Constructor
        """
        self._backup_path = None

    def read_file(self, file_path):
        '''
        It reads the file
        :param file_path: The path where the file is in the system
        :type file_path: str
        '''
        pass

    def write_file(self, file_path, content, mode='a', backup=False):
        '''
        It writes the file with the option to have a backup and different modes
        :param file_path: The path where the file is in the system
        :type file_path: str
        :param content: The content to write into the file
        :type content: str
        :param mode: The mode to write the file (overwrite, etc..)
        :type mode: str
        :param backup: Flag to create a backup file
        :type backup: boolean
        '''
        # Create backup if need it
        if backup:
            self.create_backup(file_path)
        
        # Open file
        with open(file_path, mode) as utils_file:
            # Make sure is a new line
            utils_file.write('\n')
            # Write Function
            utils_file.write(content)
            utils_file.write('\n')

    def create_backup(self, file_path):
        '''
        It creates a backup file of the current python file
        :param file_path: The path where to save the backup
        :type file_path: str
        '''
        path_without_ext = file_path.split('.py')[0]
        self._backup_path = "%s%s.py" % (path_without_ext, '_backup')
        copy2(file_path, self._backup_path)

    def delete_backup(self):
        '''
        It deletes the backup file
        '''
        if path.exists(self._backup_path):
            remove(self._backup_path)

    def rollback(self, file_path):
        '''
        It roll back the python file with the backup file
        :param file_path: The python file to get rollback
        :type file_path: str
        '''
        move(self._backup_path, file_path)
