from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QFormLayout, QLineEdit, QHBoxLayout, QDockWidget, QMainWindow, QTextEdit, QListWidget, QLabel, QListWidgetItem, QVBoxLayout, QPushButton, QListView, QTableWidget
from PyQt5.QtGui import QDesktopServices, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QEvent
from model_utils import AnvnPreModel
from widget_utils import AnvnQDockWidget

class AnvnDataVisualizationWidget(AnvnQDockWidget):
    def __init__(self, title='Data Visualization ', parent=None):
        super(AnvnDataVisualizationWidget, self).__init__(title, parent)
        self.setStatusTip(title)