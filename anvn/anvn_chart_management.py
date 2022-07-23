from anvn_widget_utils import AnvnDockWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from anvn_chart import AnvnChart

class AnvnChartManagement(QMainWindow):
    def __init__(self, data, title, parent=None):
        super().__init__()
        self.main_widget = AnvnDockWidget(title, parent, title_color='#2c2c2c', title_background='#f0f0f0')
        self.setMinimumHeight(36)
        self.data = data
        self.setStatusTip(title)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.main_widget)
        self.main_widget.set_title_double_clicked(self.__double_click_func)
        self.title_double_clicked_func = None
        self.__set_style()
        self.chart = AnvnChart()
        # self.main_widget.setWidget(self.chart)
        self.chart.run()

    def clear(self):
        self.main_widget.setWidget(None)
    
    def open(self):
        self.main_widget.setWidget(self.chart)

    def set_title_double_clicked(self, func):
        self.title_double_clicked_func = func

    def __set_style(self):
        self.setStyleSheet('''
            QMainWindow {
                border-radius: 5px;
            }
        ''')

    def __double_click_func(self):
        if self.title_double_clicked_func is not None:
            self.title_double_clicked_func(self)
        

class AnvnLastHiddenStateChartManagement(AnvnChartManagement):
    def __init__(self, data, title, parent=None):
        super().__init__(data, title, parent)

class AnvnPoolerChartManagement(AnvnChartManagement):
    def __init__(self, data, title, parent=None):
        super().__init__(data, title, parent)

class AnvnHiddenStatesChartManagement(AnvnChartManagement):
    def __init__(self, data, title, parent=None):
        super().__init__(data, title, parent)

class AnvnAttentionsChartManagement(AnvnChartManagement):
    def __init__(self, data, title, parent=None):
        super().__init__(data, title, parent)
        