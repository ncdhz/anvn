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
        self.pre_model = AnvnPreModel(model_path)

        self.dataset = AnvnDataset()
        self.model_run = AnvnModelRun()

        self.pre_model.signal_connect(self.pre_model_init_func)
        self.data_input_widget = AnvnDataInputWidget(parent=self, callback_func=self.get_input_data)
        self.data_input_widget.set_run_disabled(True, 'Wait for the model to load')

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.data_input_widget)

        self.model_operation_widget = AnvnModelOperationWidget(
            parent=self, callback_func=self.add_visualization_widget)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.model_operation_widget)

        self.pre_model.start()
    
    def add_visualization_widget(self, table):
        data_visualization_widget = AnvnDataVisualizationWidget(parent=self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, data_visualization_widget)
        self.model_operation_widget.set_callback_func(data_visualization_widget.data_monitor)
        data_visualization_widget.data_monitor(table)

    def get_input_data(self, data_list):
        self.model_operation_widget.widget_reset()
        self.data_input_widget.set_run_disabled(True, 'Waiting for model execution')
        self.dataset.set_data_list(data_list)
        self.dataset.signal_connect(self.dataset_run_func)
        self.dataset.start()
    
    def dataset_run_func(self, index):
        if index == AnvnDataset.success:
            self.model_run.set_data_loader(self.dataset.get_dataset(), self.pre_model.get_tokenizer())
            self.model_run.signal_connect(self.model_run_func)
            self.model_operation_widget.set_data_load_value(100)
            self.model_operation_widget.set_data_load_text('Data processing completed:')
            self.model_run.start()
        else:
            self.model_operation_widget.set_data_load_value(int(index / len(self.dataset) * 100))
            
    
    def model_run_func(self, index):
        if index == AnvnModelRun.success:
            self.model_operation_widget.set_tokenizer(self.pre_model.get_tokenizer()).set_outputs(self.model_run.get_outputs()).set_all_ots(self.model_run.get_all_ots()).sel_all_iis(self.model_run.get_all_iis())
            self.model_operation_widget.set_model_run_value(100)
            self.model_operation_widget.set_model_load_text('Model running completed:')
            self.data_input_widget.set_run_disabled(False, '')
            self.model_operation_widget.disabled(False)
        else:
            self.model_operation_widget.set_model_run_value(int(index / len(self.model_run) * 100))

    def pre_model_init_func(self):
        self.data_input_widget.set_run_disabled(False, '')
        self.model_operation_widget.set_model_load_text('Model loading completed:')
        self.model_operation_widget.model_load_stop()
        self.dataset.set_tokenizer(self.pre_model.get_tokenizer())
        self.model_run.set_model(self.pre_model.get_model())
