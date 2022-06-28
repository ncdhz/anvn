from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMainWindow
from PyQt5.QtCore import Qt
from data_input_widget import AnvnDataInputWidget
from data_visualization_widget import AnvnDataVisualizationWidget
from model_operation_widget import AnvnModelOperationWidget
from model_utils import AnvnPreModel

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
        self.anvn_pre_model.signal_connect(self.pre_model_init_func)
        self.anvn_pre_model_init_success = False
        self.anvn_data_input_widget = AnvnDataInputWidget(parent=self, callback_func=self.get_input_data)
        self.anvn_data_input_widget.set_run_disabled(True, 'Wait for the model to load')
        self.anvn_pre_model.start()

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.anvn_data_input_widget)
        self.anvn_model_operation_widget = AnvnModelOperationWidget(
            parent=self)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.anvn_model_operation_widget)
        self.anvn_data_visualization_widget = AnvnDataVisualizationWidget(
            parent=self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                           self.anvn_data_visualization_widget)
    
    def get_input_data(self, data_list):
        self.anvn_data_input_widget.set_run_disabled(True, 'Waiting for model execution')
        anvn_data_loader = self.anvn_pre_model.data_process(data_list)
        outputs,  all_ots, all_iis = self.anvn_pre_model.model_run(anvn_data_loader)
        self.anvn_data_input_widget.set_run_disabled(False, '')
        self.anvn_model_operation_widget.injection_data(outputs,  all_ots, all_iis)

    def pre_model_init_func(self):
        self.anvn_pre_model_init_success = True
        self.anvn_model_operation_widget.init_tokenizer(self.anvn_pre_model.get_tokenizer())
        self.anvn_data_input_widget.set_run_disabled(False, '')