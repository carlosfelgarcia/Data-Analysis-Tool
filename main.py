'''
Created on Oct 12, 2016

@author: Carlos Garcia - carlos@carlosgarcia.co
'''

# BuiltIn Imports
import os

# Internal Classes
import data_factory
import data_analysis
import plot_generator


class Main(object):
    '''
    This is the main class, all of the functions get trigger from here
    '''

    def __init__(self):
        '''Constructor'''
        self._factory = data_factory.DataFactory()
        self._current_py_handle = None
        self._data_analysis = data_analysis.DataAnalysis()
        self._plot_generator = plot_generator.PlotGenerator()
        self._plot_func_list = dir(self._plot_generator)

    def get_dataframe_file(self, path):
        """
        It get the handle from the factory and then creates a new dataframe
        from the file.
        
        Args:
            path: The path of the file.
        """
        if os.path.exists(path):
            _, ext = os.path.splitext(path)
            handle = self._factory.get_class(ext)()
            if not handle:
                return
            data_frame = handle.read_file(path)
            self._data_analysis.add_data_frame(data_frame)
            self._data_analysis.set_data_frame(-1)
    
    def set_current_data_frame(self, index):
        """It sets the data frame according to what the user is looking."""
        self._data_analysis.set_data_frame(index)
        
    def add_new_fucntion(self, name, function):
        """
        This method check if the function exist, if it does not exist it gets a
        python handle and trigger a method to add a new function into the
        data_functions file from the data_analysis class.
        
        Args:
            name: The name of the function that will be added.
            function: The function to be added into the file.
        """
        # Make sure is a new function
        if name in self._data_analysis.get_function_list():
            return 0
        self._current_py_handle = self._factory.get_class('.py')()
        if not self._data_analysis.add_function(name, function,
                                                self._current_py_handle):
            return -1
        self._data_analysis.delete_backup()
        self._current_py_handle = None
        return 1
    
    def add_new_column(self, new_col_name, cols_names, fun_name):
        """
        It triggers the addition of the column base on the new column name, the
        columns used on the function and the function name.
        
        Args:
            new_col_name: The name of the new column.
            cols_name: A list of columns that the function use.
            fun_name: The function use to add the new column.
        """
        self._data_analysis.add_new_column(new_col_name, cols_names, fun_name)
    
    def get_plot_functions(self):
        """
        It creates a list of available functions to be chosen by the user to
        create a plot.
        """
        func_list = []
        for fun in self._plot_func_list:
            if not (fun.startswith('_') or fun.startswith('get')):
                func_list.append(fun)
        return func_list
    
    def get_plot(self, values, graph, df=None):
        """
        It gets the method from the plot generator and base on the values it
        creates the plot.
        
        Args:
            values: The values used to create the plot.
            graph: The method that is going to be use to create the plot.
            
        Kwargs:
            df: The dataframe that is going to be use to create the plot.
        """
        if not df:
            df = self._data_analysis.get_data_frame()
        function = getattr(self._plot_generator, graph)
        return function(df, values)
    
    def save_df(self, file_path):
        """
        It saves the current data_frame into a specific path.
        
        Args:
            file_path: The path where the data frame is going to be save.
        """
        # Get the data frame
        df = self._data_analysis.get_data_frame()
        
        # Get the file handle
        _, ext = os.path.splitext(file_path)
        handle = self._factory.get_class(ext)()
            
        if not handle:
            return
        handle.write_file(file_path, df)
        
    def del_column(self, column_names):
        """
        It triggers a deletion of a column from the data frame.
        
        Args:
            column_names: The names of the columns to be delete.
        """
        self._data_analysis.del_column(column_names)
    
    def get_plot_label(self, func_name):
        """
        It ask for the label to be show in the UI base on the selected
        function.
        
        Agrs:
            func_name: The name of the function selected.
        """
        return self._plot_generator.get_label(func_name)
    
    def get_information(self, column_name, operation):
        """
        It gets a specific information base on the column and the operation
        selected.
        
        Args:
            column_name: The name of the selected column.
            operation: The name of the selected operation.
        """
        return self._data_analysis.get_information(column_name, operation)
    
    def get_data_frame(self):
        """It gets the current data frame."""
        return self._data_analysis.get_data_frame()

