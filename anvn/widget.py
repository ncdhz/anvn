from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QFormLayout, QLineEdit, QHBoxLayout, QDockWidget, QMainWindow
from PyQt5.QtCore import Qt

class AnvnTabWidget(QTabWidget):
    def __init__(self, main_window: QMainWindow) -> None:
        super(QTabWidget, self).__init__(main_window)
        self.main_window = main_window
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.tab_close)
        self.tab.connect(self.tab_changed)

    def tab_close(self, index):
        self.tabBar().removeTab(index)

    def tab_changed(self, index):
        self.setStatusTip(self.tabText(index))
        

    def add_widget(self, model_path='bert-base-uncased'):
        tab_name = model_path
        if len(tab_name) > 20:
            tab_name = model_path[:8] + '...' + model_path[-8:]
        self.addTab(AnvnWidget(self.main_window, model_path), tab_name)

class AnvnWidget(QMainWindow):
    def __init__(self, main_window, model_path) -> None:
        super(AnvnWidget, self).__init__(main_window)
        self.setStatusTip(model_path)