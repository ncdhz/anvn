from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMainWindow
from PyQt5.QtCore import Qt
from data_input_widget import AnvnDataInputWidget
from data_visualization_widget import AnvnDataVisualizationWidget
from model_operation_widget import AnvnModelOperationWidget
from model_utils import AnvnPreModel, AnvnDataset, AnvnModelRun

class AnvnTabWidget(QTabWidget):
    def __init__(self, main_window: QMainWindow) -> None:
        super(QTabWidget, self).__init__(main_window)
        self.main_window = main_window
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.tab_close)

    def tab_close(self, index):
        self.removeTab(index)

    def add_widget(self, model_path='bert-base-uncased'):
        tab_name = model_path
        if len(tab_name) > 20:
            tab_name = model_path[:8] + '...' + model_path[-8:]
        self.addTab(AnvnWidget(self.main_window, model_path), tab_name)

class AnvnWidget(QMainWindow):
    
    def __init__(self, main_window, model_path) -> None:
        super(AnvnWidget, self).__init__(main_window)
        self.setStatusTip(model_path)
        self.anvn_pre_model = AnvnPreModel(model_path)

        self.anvn_dataset = AnvnDataset()
        self.anvn_model_run = AnvnModelRun()

        self.anvn_pre_model.signal_connect(self.pre_model_init_func)
        self.anvn_data_input_widget = AnvnDataInputWidget(parent=self, callback_func=self.get_input_data)
        self.anvn_data_input_widget.set_run_disabled(True, 'Wait for the model to load')

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.anvn_data_input_widget)

        self.anvn_model_operation_widget = AnvnModelOperationWidget(
            parent=self)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.anvn_model_operation_widget)
        
        self.anvn_pre_model.start()

        # self.anvn_data_visualization_widget = AnvnDataVisualizationWidget(
        #     parent=self)
        # self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
        #                    self.anvn_data_visualization_widget)
    
    def get_input_data(self, data_list):
        self.anvn_model_operation_widget.widget_reset()
        self.anvn_data_input_widget.set_run_disabled(True, 'Waiting for model execution')
        self.anvn_dataset.set_data_list(data_list)
        self.anvn_dataset.signal_connect(self.dataset_run_func)
        self.anvn_dataset.start()
    
    def dataset_run_func(self, index):
        if index == AnvnDataset.success:
            self.anvn_model_run.set_data_loader(self.anvn_dataset.get_dataset(), self.anvn_pre_model.get_tokenizer())
            self.anvn_model_run.signal_connect(self.model_run_func)
            self.anvn_model_operation_widget.set_data_load_value(100)
            self.anvn_model_operation_widget.set_data_load_text('Data processing completed:')
            self.anvn_model_run.start()
        else:
            self.anvn_model_operation_widget.set_data_load_value(int(index / len(self.anvn_dataset) * 100))
            
    
    def model_run_func(self, index):
        if index == AnvnModelRun.success:
            self.anvn_model_operation_widget.set_tokenizer(self.anvn_pre_model.get_tokenizer()).set_outputs(self.anvn_model_run.get_outputs()).set_all_ots(self.anvn_model_run.get_all_ots()).sel_all_iis(self.anvn_model_run.get_all_iis())
            self.anvn_model_operation_widget.set_model_run_value(100)
            self.anvn_model_operation_widget.set_model_load_text('Model running completed:')
            self.anvn_data_input_widget.set_run_disabled(False, '')
            self.anvn_model_operation_widget.disabled(False)
        else:
            self.anvn_model_operation_widget.set_model_run_value(int(index / len(self.anvn_model_run) * 100))

    def pre_model_init_func(self):
        self.anvn_data_input_widget.set_run_disabled(False, '')
        self.anvn_model_operation_widget.set_model_load_text('Model loading completed:')
        self.anvn_model_operation_widget.model_load_stop()
        self.anvn_dataset.set_tokenizer(self.anvn_pre_model.get_tokenizer())

        self.anvn_model_run.set_model(self.anvn_pre_model.get_model())
