from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from resources import *
from PyQt5.QtWidgets import QMainWindow
from widget import AnvnTabWidget

class AnvnAction:
    def __init__(self, main_window: QMainWindow, central_widget: AnvnTabWidget) -> None:
        self.model_loading_action = QAction('Model loading', main_window)
        self.central_widget = central_widget
        self.action_init()

    def action_init(self):
        self.action_init_template(self.model_loading_action, ':/model_load',
                                  'Ctrl+L', 'Load NLP pre training model', self.model_loading_func)

    def model_loading_func(self):
        self.central_widget.add_widget()

    def action_init_template(self, action, icon_name=None, shortcut=None, tip=None, callback_func=None):
        if icon_name:
            action.setIcon(QIcon(icon_name))
        if shortcut:
            action.setShortcut(shortcut)
        if tip:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if callback_func:
            action.triggered.connect(callback_func)


class AnvnToolBar(AnvnAction):
    def __init__(self, main_window: QMainWindow, central_widget: AnvnTabWidget) -> None:
        super(AnvnToolBar, self).__init__(main_window, central_widget)
        self.file_tool_bar = main_window.addToolBar('File')
        self.file_tool_bar_init()

    def file_tool_bar_init(self):
        self.file_tool_bar.addActions([self.model_loading_action])


class AnvnMenu(AnvnAction):
    def __init__(self, main_window: QMainWindow, central_widget: AnvnTabWidget) -> None:
        super(AnvnMenu, self).__init__(main_window, central_widget)
        menu_bar = main_window.menuBar()
        self.file_menu = menu_bar.addMenu('File')
        self.file_menu_init()
    
    def file_menu_init(self):
        self.file_menu.addActions([self.model_loading_action])
