'''
Created on Nov 2, 2016

@author: Carlos Garcia - carlos@carlosgarcia.co
'''
# External Libraries Imports
import seaborn as sns


class PlotGenerator(object):
    '''
    This class handles all the graphs to be generated by the system
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._labels = {'factorplot': 'Column',
                        'factorplot_hue': 'Column, Hue'}

    def get_label(self, func_name):
        '''
        It gets the label to be display it in the UI by the function name
        :param func_name: The function name to look into the dictionary
        :type func_name: str
        '''
        return self._labels[func_name]

    def factorplot(self, df, column):
        '''
        Factor plot graph to be generated by the UI
        :param df: Data frame to use to generate the graph
        :type df: pandas.DataFrame
        :param column: The column name selected to generate the graph
        :type column: list
        '''
        if len(column) > 1:
            return
        return sns.factorplot(column[0], data=df, kind='count')

    def factorplot_hue(self, df, columns):
        '''
        Factor plot with hue graph to be display it in the UI
        :param df: Data frame to use to generate the graph
        :type df: pandas.DataFrame
        :param columns: The columns names selected to generate the graph
        :type columns: list
        '''
        if not len(columns) == 2:
            return
        return sns.factorplot(columns[0], hue=columns[1], data=df,
                              kind='count')