from anvn_widget_utils import AnvnDockWidget
class AnvnChartManagement(AnvnDockWidget):
    def __init__(self, data, title, parent=None):
        super().__init__(title, parent)
        self.data = data
        self.setStatusTip(title)

