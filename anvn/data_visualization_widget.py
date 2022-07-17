from widget_utils import AnvnDockWidget

class AnvnDataVisualizationWidget(AnvnDockWidget):
    def __init__(self, title='Data Visualization ', parent=None):
        super(AnvnDataVisualizationWidget, self).__init__(title, parent)
        self.setStatusTip(title)
    
    def data_monitor(self, data):
        pass