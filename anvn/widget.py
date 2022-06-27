from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMainWindow
from PyQt5.QtCore import Qt
from sentence_input_widget import AnvnSentenceInputWidget
from data_visualization_widget import AnvnDataVisualizationWidget
from model_operation_widget import AnvnModelOperationWidget

class AnvnTabWidget(QTabWidget):
    def __init__(self, main_window: QMainWindow) -> None:
        super(QTabWidget, self).__init__(main_window)
        self.main_window = main_window
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.tab_close)

    def tab_close(self, index):
        self.tabBar().removeTab(index)

    def add_widget(self, model_path='bert-base-uncased'):
        tab_name = model_path
        if len(tab_name) > 20:
            tab_name = model_path[:8] + '...' + model_path[-8:]
        self.addTab(AnvnWidget(self.main_window, model_path), tab_name)

class AnvnWidget(QMainWindow):
    def __init__(self, main_window, model_path) -> None:
        super(AnvnWidget, self).__init__(main_window)
        self.setStatusTip(model_path)
        # self.anvn_pre_model = AnvnPreModel(model_path)
        # central_widget = QWidget()
        # central_widget.setFixedWidth(1)
        # self.setCentralWidget(central_widget)
        self.anvn_sentence_input_widget = AnvnSentenceInputWidget(parent=self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.anvn_sentence_input_widget)
        self.anvn_model_operation_widget = AnvnModelOperationWidget(
            parent=self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.anvn_model_operation_widget)
        self.anvn_data_visualization_widget = AnvnDataVisualizationWidget(
            parent=self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                           self.anvn_data_visualization_widget)
