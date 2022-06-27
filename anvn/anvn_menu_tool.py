from PyQt5.QtWidgets import QAction, QToolBar, QMenuBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from anvn_resources import *

class AnvnAction(QAction):
    signal = pyqtSignal(str)

    def __init__(self, name, icon=None, shortcut=None, tip=None, func=None, parent=None):
        super().__init__(name, parent=parent)
        if icon is not None:
            self.setIcon(QIcon(icon))
        
        if shortcut is not None:
            self.setShortcut(shortcut)

        if tip is not None:
            self.setToolTip(tip)
            self.setStatusTip(tip)
        
        if func is not None:
            self.triggered.connect(func)

def action_analysis(action_dicts, parent, tool_bar=False):
    actions = []
    for action_dict in action_dicts:
        if not tool_bar:
            actions.append(AnvnAction(**action_dict, parent=parent))
        else:
            action = {
                'name': action_dict.get('name', None),
                'icon': action_dict.get('icon', None),
                'shortcut': None,
                'tip': action_dict.get('tip', None),
                'func': action_dict.get('func', None),
            }
            actions.append(AnvnAction(**action, parent=parent))
    return actions
        

class AnvnToolBar(QToolBar):
    def __init__(self, title, actions):
        super().__init__(title)
        self.addActions(action_analysis(actions, self, True))

class AnvnMenuBar(QMenuBar):
    def __init__(self, menu):
        super().__init__()
        for action_key in menu:
            menu_ = self.addMenu(action_key)
            menu_.addActions(action_analysis(menu[action_key], self))
