'''
Created on Oct 25, 2016

@author: Carlos Garcia - carlos@carlosgarcia.co
'''
# Internal Imports
import data_functions


class DataAnalysis(object):
    """This class is in charge of all the logic that involve data frames"""

    def __init__(self):
        """
        Constructor of DataAnalysis class
        """
        self._data_frame = None
        self._function_list = dir(data_functions)
        self._function_path = 'data_functions.py'
        self._data_frame_list = []
        
    def add_data_frame(self, data_frame):
        """
        This method add a new data frame into the list of data frames.
        
        Args: 
            data_frame: The new data frame to be added.
        
        """
        self._data_frame_list.append(data_frame)
        
    def set_data_frame(self, index):
        """
        This method keep update on the data frame that is selected by the user.
        
        Args:
            index: This is usually the index of the table and it should match
            with the index on the UI tab.
        """
        self._data_frame = self._data_frame_list[index]
        
    def get_data_frame(self):
        """This method return the current data frame"""
        return self._data_frame
    
    def add_function(self, name, function, py_handle):
        """
        This method add a new function into a specific path, this path should
        be the data_functions.py but it might vary.
        
        Args:
            name: This is the name of the function to be added
            function: This is the function it self.
            py_handle: This is a python handle that comes from the main class.
            
        Return: True if succeed or False is there is a syntax error in the
                new function.
        """
        py_handle.write_file(self._function_path, function, 'a', True)
        try:
            reload(data_functions)
            self._function_list.append(name)
            return True
        except SyntaxError:
            py_handle.rollback(self._function_path)
            return False
    
    def get_function_list(self):
        """This method return the list of function in data_functions.py."""
        return self._function_list
    
    def add_new_column(self, new_col_name, cols_names, fun_name):
        """
        This method add a new column into the current data frame.
        
        Args:
            new_col_name: The name of the new column.
            cols_names: The names of the columns that are going to be use to
                        generate the new column.
            fun_name: The name of the function that is going to be use.
        """
        function = getattr(data_functions, fun_name)
        try:
            list_p = []
            new_column = self._data_frame[cols_names].apply(function,
                                                            axis=1,
                                                            args=(list_p,))
        except TypeError:
            new_column = self._data_frame[cols_names].apply(function,
                                                            axis=1)
        self._data_frame[new_col_name] = new_column
    
    def del_column(self, column_names):
        """
        This method delete the columns (it could be one or more) from the
        current data frame.
        
        Args:
            column_names: It is a list of names of the columns that are going
            to be drop.
        """
        self._data_frame = self._data_frame.drop(column_names, axis=1)
    
    def get_information(self, column_name, operation):
        """
        This method is to do simple operations on the column.
        
        Args:
            column_name: The name of the column where the operation will be
                         implemented.
            operation: The operation to implement.
        """
        if operation == 'Mean':
            try:
                return str(self._data_frame[column_name].mean())
            except TypeError:
                return
        elif operation == 'Value Count':
            info = self._data_frame[column_name].value_counts().to_dict()
            value = ''
            for k, v in info.iteritems():
                value += ': '.join((str(k), str(v)))
                value += '\n'
            return value
