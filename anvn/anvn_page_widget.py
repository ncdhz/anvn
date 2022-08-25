from PyQt5.QtWidgets import QMainWindow, QTabWidget
from PyQt5.QtCore import Qt, pyqtSignal
from anvn_data_input_widget import AnvnDataInputWidget
from anvn_data_visualization_widget import AnvnDataVisualizationWidget
from anvn_data_operation_widget import AnvnDataOperationWidget
from anvn_model_utils import AnvnPreModel, AnvnDataset, AnvnModelRun, AnvnModelInfo
from anvn_select_model_widget import AnvnSelectModelWidget
from anvn_utils import AnvnUtils

class AnvnTabWidget(QTabWidget):

    tab_null = pyqtSignal()

    def __init__(self):
        super(QTabWidget, self).__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.tab_close)

    def tab_close(self, index):
        self.removeTab(index)
        if self.count() == 0:
            self.tab_null.emit()

    def load_model(self, model_names, tokenizer_names, remove=True):
        index = 0
        if remove:
            index = self.currentIndex()
            self.removeTab(index)
        widget, tab_name = self.init_model(model_names, tokenizer_names)
        self.insertTab(index, widget, tab_name)
        self.setCurrentWidget(widget)

    def __model_error_func(self, widget, error_message):
        index = self.indexOf(widget)
        self.removeTab(index)
        select_model = AnvnSelectModelWidget(error_message=error_message)(self.load_model)
        self.insertTab(index, select_model, 'Select Model')

    def init_model(self, model_names, tokenizer_names):
        
        widget = AnvnWidget(model_names, tokenizer_names)
        widget.error.connect(self.__model_error_func)
        return widget, AnvnUtils.middle_text_omission(','.join(model_names), 20)

class AnvnWidget(QMainWindow):

    error = pyqtSignal(QMainWindow, str)

    def __init__(self, model_names, tokenizer_names) -> None:
        super().__init__()
        self.__status_tip = AnvnUtils.middle_text_omission(','.join(model_names), 20)
        self.setStatusTip(self.__status_tip)

        self.pre_model = AnvnPreModel(model_names, tokenizer_names)
        self.pre_model.handle.connect(self.__pre_model_init_func)

        self.dataset = AnvnDataset()
        self.dataset.handle.connect(self.__dataset_run_func)

        self.model_run = AnvnModelRun()
        self.model_run.handle.connect(self.__model_run_func)

        
        self.data_input_widget = AnvnDataInputWidget(parent=self)
        self.data_input_widget.set_run_disabled(True, 'Wait for the model to load')
        self.data_input_widget.handle.connect(self.__get_input_data)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.data_input_widget)

        self.data_operation_widget = AnvnDataOperationWidget()
        self.lmo_widget = self.data_operation_widget.set_lmo_widget()
        self.data_operation_widget.handle.connect(self.__data_operation_func)


        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.data_operation_widget)

        self.data_visualization_widget = None
        self.pre_model.start()
    
    def __data_operation_func(self):
        mmo = self.data_operation_widget.injection_data(self.model_run.get_model_output())
        mmo.handle.connect(self.__add_visualization_func(mmo.get_config()))

    

    def __add_visualization_func(self, config):
        def av(table_data):
            if self.data_visualization_widget is None:
                self.data_visualization_widget = AnvnDataVisualizationWidget(config)
                self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.data_visualization_widget)
                self.data_visualization_widget.handle.connect(self.__remove_visualization_func)

            self.data_visualization_widget.data_monitor(table_data)
        return av

    def __remove_visualization_func(self):
        if self.data_visualization_widget is not None:
            self.removeDockWidget(self.data_visualization_widget)
            self.data_visualization_widget = None

    def __get_input_data(self, data_list):
        self.data_input_widget.set_run_disabled(True, 'Waiting for model execution')
        self.data_operation_widget.widget_reset()
        self.dataset.set_data(data_list)
        self.dataset.start()
    
    def __dataset_run_func(self, index):
        if index == AnvnModelInfo.success:
            self.model_run.set_data_loaders(self.dataset.get_data_loaders())
            self.lmo_widget.set_data_load_value(100)
            self.lmo_widget.set_data_load_text('Data processing completed:')
            self.model_run.start()
        elif index == AnvnModelInfo.error:
            self.lmo_widget.set_error_message('Data processing error, please check the data.')
            self.data_input_widget.set_run_disabled(False)
        else:
            self.lmo_widget.set_data_load_value(int(index / len(self.dataset) * 100))
        
    def __model_run_func(self, index):
        if index == AnvnModelInfo.success:
            self.lmo_widget.set_model_run_value(100)
            self.lmo_widget.set_model_run_text('Model running completed:')
            self.data_input_widget.set_run_disabled(False, '')
            self.lmo_widget.show_disabled(False)
        elif index == AnvnModelInfo.error:
            self.lmo_widget.set_error_message('Model running error, please check the model.')
            self.data_input_widget.set_run_disabled(False)
        else:
            self.lmo_widget.set_model_run_value(int(index / len(self.model_run) * 100))

    def __pre_model_init_func(self, index):
        if index == AnvnModelInfo.success:
            self.lmo_widget.set_model_load_text('Model loading completed:')
            self.lmo_widget.model_load_stop()
            self.dataset.set_model_data(self.pre_model.get_model_data())
            self.model_run.set_model_data(self.pre_model.get_model_data())
            self.data_input_widget.set_run_disabled(False, '')
        elif index == AnvnModelInfo.error:
            self.error.emit(self, f'Model [{self.__status_tip}] loading error.')
            