'''
Created on Oct 12, 2016

@author: Carlos Garcia - carlos@carlosgarcia.co
'''
# PyQt imports
import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

# Built-in imports
import sys
import collections

# External libraries Imports
import numpy as np

# Core imports
import main

# Constants
TABLE_SIZE = 700
INFO = ['Mean', 'Value Count']


class MainWindow(qg.QMainWindow):
    '''
    MainWindow
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Variables
        self._actions = []
        self._menus = []
        
        # Main Window
        qg.QMainWindow.__init__(self)
        self.setWindowTitle('Data Analysis Tool')
        pos = qg.QApplication.desktop().cursor().pos()
        screen = qg.QApplication.desktop().screenNumber(pos)
        centerPoint = qg.QApplication.desktop().screenGeometry(screen).center()
        self.setGeometry(centerPoint.x() / 2, centerPoint.y() / 2, 1020, 720)
        
        # Add menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        
        # Add file actions & sub-menus
        self._create_actions()
        file_menu.addActions(self._actions)
        self._add_sub_menus(file_menu)

    def _add_sub_menus(self, file_menu):
        """
        This method add the needed sub menus.
        
        Args:
            file_menu: the main menu for files.
        """
        # ------------------- Load Data SubMenu Start -------------------------
        # Add Menu
        load_menu = qg.QMenu('&Load Data', self)
        file_menu.insertMenu(self._actions[-1], load_menu)
        
        # Add Actions
        action_file = qg.QAction("&Load Data From File", self)
        action_file.setStatusTip("Load data from file")
        
        action_spider = qg.QAction("&Send Spider", self)
        action_spider.setStatusTip("Send Spider and load data")
        
        load_menu.addAction(action_file)
        load_menu.addAction(action_spider)
        
        # Connections
        action_file.triggered.connect(self._load_file)
        action_spider.triggered.connect(self._send_spider)
        # ------------------- Load Data SubMenu End -------------------------
    
    def _create_actions(self):
        '''
        This method create and add actions on the menu file to a pre-existing
        list.
        '''
        # Menu actions
        quit_action = qg.QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit the app")
        
        save_action = qg.QAction("&Save DataFrame", self)
        save_action.setShortcut("Ctrl+s")
        save_action.setStatusTip("Save DataFrame to csv file")
        
        # Connections
        quit_action.triggered.connect(self._close_window)
        save_action.triggered.connect(self._save_df)
        
        # Add Actions to the list
        self._actions.append(save_action)
        self._actions.append(quit_action)
        
    def _close_window(self):
        """
        This method close the main window.
        """
        main_dialog = self.centralWidget()
        msn = 'Are you sure you want to quit?'
        ans = main_dialog.default_question(msn)
        if ans:
            sys.exit()
        
    def _load_file(self):
        """
        This method open a window to choose the file and trigger the creation
        of a table.
        """
        main_dialog = self.centralWidget()
        tittle = 'Choose the file you want to load'
        file_path = str(qg.QFileDialog.getOpenFileName(self, tittle))
        main_dialog.create_table_file(file_path)
        
    def _send_spider(self):
        """
        This method will be implement soon, but it will trigger a spider to
        claw information from the web.
        """
        print 'Coming soon'
        
    def _save_df(self):
        """
        This method open a window to choose where to save the file and trigger
        the functions to save the data frame.
        """
        tittle = 'Choose the path where you want to save the file'
        op = qg.QFileDialog.ReadOnly
        file_path = qg.QFileDialog.getSaveFileName(self,
                                                   tittle,
                                                   filter='*.csv',
                                                   options=op)
        # Get the QDialog
        main_dialog = self.centralWidget()
        main_dialog.main.save_df(str(file_path))


class MainDialog(qg.QDialog):
    """
    This is the main dialog.
    """
    def __init__(self, main):
        """
        Constructor
        """
        qg.QDialog.__init__(self)
        
        # World instance
        self.main = main
        
        self._loaded = False
        self.setLayout(qg.QHBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(2)
        
        # Fonts
        font = qg.QFont()
        font.setBold(True)
        font.setCapitalization(qg.QFont.Capitalize)
        font.setPixelSize(12)
        
        font_disclaimer = qg.QFont()
        font_disclaimer.setPixelSize(12)
        
        # Main Widget
        main_widget = qg.QWidget()
        
        # Main Layout
        main_layout = qg.QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(50)
        
        # ---------------- Left Side UI --------------------------
        main_left_layout = qg.QVBoxLayout()
        main_left_layout.setContentsMargins(5, 5, 5, 5)
        main_left_layout.setSpacing(10)
        
        # ---------------------- Add column ----------------------
        col_widget = qg.QWidget()
        col_widget.setFixedHeight(400)
        col_widget.setFixedWidth(450)
        add_col_layout = qg.QVBoxLayout()
        col_widget.setLayout(add_col_layout)
        col_widget.layout().setAlignment(qc.Qt.AlignTop)
        col_widget.layout().setSpacing(5)
        
        new_col_lb = qg.QLabel('Add new Column')
        new_col_lb.setFont(font)
        new_col_lb.setAlignment(qc.Qt.AlignHCenter)
        new_col_name_lb = qg.QLabel('New column name')
        new_col_name_lb.setFont(font)
        self._txt_new_col_name = qg.QLineEdit()
        self._txt_new_col_name.setMinimumWidth(400)
        
        cols_names_lb = qg.QLabel('Columns')
        cols_names_lb.setFont(font)
        cols_dis_lb = qg.QLabel('Valid column names separated by commas')
        cols_dis_lb.setFont(font_disclaimer)
        self._txt_cols_names = qg.QLineEdit()
        
        col_funct_name_lb = qg.QLabel('Function name')
        col_funct_name_lb.setFont(font)
        self._clean_txt = 0
        self._txt_col_funct_name = qg.QLineEdit()
        reg_ex = qc.QRegExp("[a-z0-9_]+")
        text_validator = qg.QRegExpValidator(reg_ex, self._txt_col_funct_name)
        self._txt_col_funct_name.setValidator(text_validator)
        col_function_lb = qg.QLabel('Function')
        col_function_lb.setFont(font)
        self._txt_col_function = qg.QTextEdit()
        self._txt_col_function.setMaximumHeight(150)
        
        # Set default values
        self._set_default_values()
        
        self._btn_add_col = qg.QPushButton('Add Column')
        self._btn_delete_column = qg.QPushButton('Delete Column(s)')
        
        # Add widgets to column layout
        add_col_layout.addWidget(new_col_lb)
        add_col_layout.addWidget(new_col_name_lb)
        add_col_layout.addWidget(self._txt_new_col_name)
        add_col_layout.addWidget(cols_names_lb)
        add_col_layout.addWidget(cols_dis_lb)
        add_col_layout.addWidget(self._txt_cols_names)
        add_col_layout.addWidget(col_funct_name_lb)
        add_col_layout.addWidget(self._txt_col_funct_name)
        add_col_layout.addWidget(col_function_lb)
        add_col_layout.addWidget(self._txt_col_function)
        add_col_layout.addWidget(self._btn_add_col)
        add_col_layout.addWidget(self._btn_delete_column)
        
        # -------------------- Plot Layout ----------------------------
        plot_widget = qg.QWidget()
        plot_layout = qg.QVBoxLayout()
        plot_widget.setLayout(plot_layout)
        plot_layout.setSpacing(4)
        plot_layout.setAlignment(qc.Qt.AlignTop)
        
        data_analysis_lb = qg.QLabel('Data Analysis')
        data_analysis_lb.setFont(font)
        data_analysis_lb.setAlignment(qc.Qt.AlignHCenter)
        plot_type_lb = qg.QLabel('Plot type')
        plot_type_lb.setFont(font)
        
        self._plot_menu = qg.QComboBox()
        self._plot_menu.addItems(self.main.get_plot_functions())
        
        self._column_names_lb = qg.QLabel('Attributes: Column')
        self._column_names_lb.setFont(font)
        self._txt_col_names = qg.QLineEdit()
        
        self._btn_plot = qg.QPushButton('Show Plot')
        
        # Add widgets to plot layout
        plot_layout.addWidget(data_analysis_lb)
        plot_layout.addWidget(plot_type_lb)
        plot_layout.addWidget(self._plot_menu)
        plot_layout.addWidget(self._column_names_lb)
        plot_layout.addWidget(self._txt_col_names)
        plot_layout.addWidget(self._btn_plot)
        
        # -------------------- Additional info -----------------------
        info_widget = qg.QWidget()
        info_layout = qg.QVBoxLayout()
        info_widget.setLayout(info_layout)
        info_layout.setSpacing(4)
        info_layout.setAlignment(qc.Qt.AlignTop)
        
        add_info_lb = qg.QLabel('Additional Information')
        add_info_lb.setFont(font)
        add_info_lb.setAlignment(qc.Qt.AlignHCenter)
        
        disclaimer_lb = qg.QLabel('Select the column you want to get the '
                                  'information from')
        disclaimer_lb.setFont(font_disclaimer)
        
        info_type_lb = qg.QLabel('Request Info')
        info_type_lb.setFont(font)
        
        self._info_menu = qg.QComboBox()
        self._info_menu.addItems(INFO)
        
        self._btn_info = qg.QPushButton('Get Information')
        
        info_layout.addWidget(add_info_lb)
        info_layout.addWidget(disclaimer_lb)
        info_layout.addWidget(info_type_lb)
        info_layout.addWidget(self._info_menu)
        info_layout.addWidget(self._btn_info)
        
        # Add main widgets
        main_left_layout.addWidget(col_widget)
        main_left_layout.addWidget(plot_widget)
        main_left_layout.addWidget(info_widget)

        # ---------------- Right Side UI --------------------------
        
        # Tab Widget
        self._tab_widget = qg.QTabWidget()
        self._tab_widget.setTabPosition(0)
        
        # Table Layout
        self._table_layout = qg.QHBoxLayout()
        self._table_layout.setContentsMargins(5, 5, 5, 5)
        self._table_layout.setAlignment(qc.Qt.AlignTop)
        
        # Table widget
        self.new_table_widget()
        
        # Added Main Layout
        main_layout.addLayout(main_left_layout)
        main_layout.addLayout(self._table_layout)
        main_widget.setLayout(main_layout)
        
        self.layout().addWidget(main_widget)
        
        # Disable UI until a data frame is loaded
        self.set_enable_ui(False)
    
        # --------------------- Connections -----------------------------
        self._btn_add_col.clicked.connect(self.add_column)
        self._btn_delete_column.clicked.connect(self.del_column)
        self._txt_col_function.selectionChanged.connect(self._clean_txt_field)
        self._txt_col_funct_name.editingFinished.connect(self._add_function_txt)
        self._btn_plot.clicked.connect(self.show_plot)
        self._btn_info.clicked.connect(self.show_info)
        # Used the other way to connect as it use the parameters
        self.connect(self._plot_menu,
                     qc.SIGNAL('currentIndexChanged(QString)'),
                     self._change_label)
        
        self.connect(self._tab_widget,
                     qc.SIGNAL('currentChanged(int)'),
                     self._change_data_frame)

    # ------------------ Class UI Methods ------------------------------
    def _change_data_frame(self, index):
        """
        This method get trigger every time the table tab change.
        
        Args:
            index: It is the index of the tab table.
        """
        self.main.set_current_data_frame(index)
    
    def create_table_file(self, file_path):
        """
        This method check if a table is already loaded, if there is a loaded
        table, it asked if the user want to overwrite the table or create a new
        tab.
        
        Args:
            file_path: is the file path of the new table to be loaded.
        """
        self.main.get_dataframe_file(file_path)
        if not self._loaded:
            self.fill_columns()
            # Enable txt, menus and btn in the ui
            self.set_enable_ui(True)
            self._loaded = True
        else:
            msn = ('A table is already loaded, do you want to open it in a new'
                   ' tab?')
            q = self.default_question(msn, 'Yes', 'No, overwrite current tab')
            # Yes = 0, No = 1
            if q == 1:
                self.fill_columns()
            else:
                self.new_table_widget()
                self.fill_columns()
        
    def new_table_widget(self):
        """It creates a new table widget in a new tab."""
        table_widget = qg.QTableWidget()
        table_widget.setMinimumWidth(TABLE_SIZE)
        table_widget.setMinimumHeight(TABLE_SIZE)
        tab_name = 'Table {0}'.format(self._tab_widget.currentIndex() + 2)
        self._tab_widget.addTab(table_widget, tab_name)
        self._tab_widget.setCurrentIndex(self._tab_widget.currentIndex() + 1)
        self._table_layout.addWidget(self._tab_widget)
    
    def set_enable_ui(self, option=True):
        """
        This method will enable the available functions on the table.
        
        Kwargs:
            option: It allow to enable or disable the controls.
        """
        self._txt_col_funct_name.setEnabled(option)
        self._txt_col_function.setEnabled(option)
        self._txt_col_names.setEnabled(option)
        self._txt_cols_names.setEnabled(option)
        self._txt_new_col_name.setEnabled(option)
        self._btn_add_col.setEnabled(option)
        self._btn_delete_column.setEnabled(option)
        self._btn_info.setEnabled(option)
        self._btn_plot.setEnabled(option)
        self._info_menu.setEnabled(option)
        self._plot_menu.setEnabled(option)
    
    def show_info(self):
        """
        This method will check if a column is selected and trigger the
        operation selected by the user, then it grabs the result and create
        a new dialog to show it.
        """
        # Get current table
        table_widget = self._tab_widget.currentWidget()
        
        # Get the values to make the request to the system
        col_selected = table_widget.selectedItems()
        if not col_selected:
            msn = 'Please select the column to get the information from.'
            self.default_warning(msn)
            return
        column_index = table_widget.column(col_selected[0])
        item = table_widget.horizontalHeaderItem(column_index)
        col_name = str(item.text())
        
        opperation = str(self._info_menu.currentText())
        
        # Get the information from the world
        value = self.main.get_information(col_name, opperation)
        if not value:
            msn = 'Some values can not be converted to numeric'
            self.default_warning(msn)
            return
        
        # Custom dialog to show the information
        self.info_dialog = qg.QDialog()
        self.info_dialog.setWindowTitle('Data Analysis Information')
        info_layout = qg.QVBoxLayout()
        
        info_lb = qg.QLabel('The "{0}" for column "{1}" is:'.format(opperation,
                                                                    col_name))
        info_txt = qg.QTextEdit()
        info_txt.setPlainText(value)
        info_txt.setReadOnly(True)
        
        info_layout.addWidget(info_lb)
        info_layout.addWidget(info_txt)
        
        self.info_dialog.setLayout(info_layout)
        self.info_dialog.show()
    
    def _change_label(self, func_name):
        """
        This method change the label that comes from the plot generator class,
        to inform the user what are the required values to show the specific
        graphic.
        
        Args:
            func_name: the function/graph selected.
        """
        label = self.main.get_plot_label(str(func_name))
        self._column_names_lb.setText('Attributes: {0}'.format(label))
    
    def del_column(self):
        """
        This method check if the columns to be deleted are selected and
        triggers the deletion function. When fill_columns method is called,
        it gets the updated values from the world.
        """
        # Get current table
        table_widget = self._tab_widget.currentWidget()
        
        # Get all the values
        col_selected = table_widget.selectedItems()
        if not col_selected:
            msn = 'Please select the columns you want to delete'
            self.default_warning(msn)
            return
        column_names = []
        last_name = ''
        for column_item in col_selected:
            column_index = table_widget.column(column_item)
            item = table_widget.horizontalHeaderItem(column_index)
            column_name = str(item.text())
            if column_name == last_name:
                continue
            last_name = column_name
            column_names.append(column_name)

        # Delete column
        self.main.del_column(column_names)
          
        # reload table values
        self.fill_columns()
        
    def add_column(self):
        """
        This method check the values needed to add the columns, it triggers the
        check to the functions that was wrote by the user and then it triggers
        the creation of the new column.
        """
        # Get all the values
        new_col_name = str(self._txt_new_col_name.text())
        cols_names = str(self._txt_cols_names.text())
        function_name = str(self._txt_col_funct_name.text())
        function = str(self._txt_col_function.toPlainText())
        
        # Check if all the values are filled
        if not self._check_fields([new_col_name, cols_names,
                                   function_name, function]):
            return
        
        # Check the columns existence
        current_data = self.main.get_data_frame()
        df_columns = current_data.keys()
        columns_list = [col_name.strip() for col_name in cols_names.split(',')]
        if not any([name in df_columns for name in columns_list]):
            self.default_warning('One of the columns does not exist, please '
                                 'check the names and try again')
            return

        # Add new function
        function_added = self.main.add_new_fucntion(function_name, function)
        if function_added == -1:
            msn = 'Error: There are some Syntax errors in your function'
            self.default_warning(msn)
            return
        elif function_added == 0:
            msn = 'This function already exist, do you want to continue?'
            ans = self.default_question(msn)
            # 0 = no 1= yes
            if not ans:
                self._clean_txt = 0
                self.default_warning('The function was not added,'
                                     ' please try again')
                return
        
        # Add the column and get the updated data frame
        self.main.add_new_column(new_col_name, columns_list,
                                 function_name)
        
        # reload table values
        self.fill_columns()
        
        # Set the UI back to default
        self._set_default_values()
        
    def _check_fields(self, fields):
        """
        This method check if the fields passed are filled.
        
        Args:
            fields: The fields to be check
        """
        for value in fields:
            if value == '' or value is None:
                self._clean_txt = 0
                self.default_warning('All the values need to be filled')
                return False
        return True
    
    def default_warning(self, msn):
        """
        This method show a default dialog whit a specific message.
        
        Args:
            msn: The message to be shown.
        """
        qg.QMessageBox.warning(self, 'main Data Analysis',
                               msn,
                               buttons=qg.QMessageBox.Ok,
                               defaultButton=qg.QMessageBox.NoButton)
        
    def default_question(self, msn, btn1='No', btn2='Yes'):
        """
        This method show a question dialog whit a specific message.
        
        Args:
            msn: The message to be shown.
        """
        return qg.QMessageBox.question(self, 'main Data Analysis',
                                       msn,
                                       btn1,
                                       btn2,
                                       defaultButtonNumber=0)
    
    def _set_default_values(self):
        """This method restore the values of the all fields."""
        self._txt_new_col_name.clear()
        self._txt_new_col_name.setPlaceholderText('Type New Column name')
        self._txt_cols_names.clear()
        self._txt_cols_names.setPlaceholderText('Type Columns names')
        self._txt_col_funct_name.clear()
        self._txt_col_funct_name.setPlaceholderText('Type Function Name')
        self._txt_col_function.setText('Type the function that relates'
                                       ' the columns, e.g...'
                                       '\ndef funct_name(*Columns):\n'
                                       '    function...')
        self._clean_txt = 0

    def _clean_txt_field(self):
        """
        This method clean the text field where to allow the user to write the
        new function.
        """
        if self._clean_txt == 0:
            self._clean_txt = 1
            self._txt_col_function.clear()
            
    def _add_function_txt(self):
        """
        This method add the first line of the function, when a name is given.
        """
        if self._clean_txt == 0:
            self._clean_txt = 1
            function_name = self._txt_col_funct_name.text()
            txt = "def %s():\n    " % function_name
            self._txt_col_function.setText(txt)
            
    def fill_columns(self):
        """
        This method get the information from the current data frame and fill a
        table by the columns.
        """
        # Get current table
        table_widget = self._tab_widget.currentWidget()
        
        # Clear table
        table_widget.setRowCount(0)
        table_widget.setColumnCount(0)
        
        # Get columns
        current_data = self.main.get_data_frame()
        columns = sorted(current_data.keys())
            
        # Add values to the table
        for column in columns:
            col_num = table_widget.columnCount()
            row_total_num = table_widget.rowCount()
            table_widget.insertColumn(col_num)
            col_item = qg.QTableWidgetItem(column)
            table_widget.setHorizontalHeaderItem(col_num, col_item)
            if isinstance(current_data[column], collections.Iterable):
                for i in xrange(len(current_data[column])):
                    value = ''
                    if isinstance(value, np.float64):
                        value = np.int(current_data[column][i])

                    elif isinstance(value, str):
                        value = str(current_data[column][i])
                        if value == 'nan':
                            value = '---'
                    
                    table_item = qg.QTableWidgetItem(value)
                    
                    if i >= row_total_num:
                        table_widget.insertRow(i)
                    table_widget.setItem(i, col_num, table_item)
            else:
                table_widget.insertRow(row_total_num)
                table_item = qg.QTableWidgetItem(current_data[column])
                table_widget.setItem(row_total_num, col_num, table_item)
                
        table_widget.resizeColumnsToContents()
        table_widget.resizeRowsToContents()
        
    def show_plot(self):
        """
        This method check the values needed and show the selected graph. It
        expect to get a FacetGrid from the world.
        """
        current_data = self.main.get_data_frame()
        vals = str(self._txt_col_names.text())
        if not vals:
            self.default_warning('Please fill the values you want to analyze')
            return
        values = [val.strip() for val in vals.split(',')]
        if any(map(lambda v: v not in current_data.keys(), values)):
            self.default_warning("Some values don't match column name")
            return
        graph = str(self._plot_menu.currentText())
        plot_graph = self.main.get_plot(values, graph)
        if not plot_graph:
            self.default_warning("The values don't match the graph you want")
            return
        plot_graph.fig.show()
    
    def mousePressEvent(self, *args, **kwargs):
        """This method clear the selected columns."""
        # Get current table
        table_widget = self._tab_widget.currentWidget()
        table_widget.clearSelection()
    
if __name__ == '__main__':
    # Main Class instance
    main = main.Main()
    
    # UI
    app = qg.QApplication(sys.argv)
    main_ui = MainWindow()
    dialog = MainDialog(main)
    main_ui.setCentralWidget(dialog)
    main_ui.show()
    sys.exit(app.exec_())
