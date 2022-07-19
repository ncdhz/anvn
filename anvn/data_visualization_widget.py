from widget_utils import AnvnDockWidget
from table_management import AnvnTableManagement
from PyQt5.QtWidgets import QListWidget, QMainWindow, QListWidgetItem
from PyQt5.QtCore import Qt
class AnvnData:
    def __init__(self, data=None, data_num=None, heads=None, layers=None, key=None, horizontal_headers=None, vertical_headers=None):
        self.data = data
        self.data_num = data_num
        self.heads = heads
        self.layers = layers
        self.key = key
        self.horizontal_headers = horizontal_headers
        self.vertical_headers = vertical_headers

class AnvnDataVisualizationWidget(AnvnDockWidget):
    def __init__(self, title='Data Visualization ', parent=None):
        super(AnvnDataVisualizationWidget, self).__init__(title, parent)
        self.setStatusTip(title)
        self.data_list = QListWidget(self)
        self.data_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.datas = []
    
    def data_monitor(self, table: AnvnTableManagement):
        data = AnvnData(data=table.get_data(), data_num=table.get_data_num(), heads=table.get_heads(), layers=table.get_layers(), key=table.get_key(), horizontal_headers=table.get_horizontal_headers(), vertical_headers=table.get_vertical_headers())
        self.add_data(data)

    def add_data(self, data):
        self.datas.append(data)
        self.__add_data_item()

    def __add_data_item(self):
        data_item, data_widget = self.__get_data_item()
        self.data_list.addItem(data_item)
        self.data_list.setItemWidget(data_item, data_widget)
    
    def __get_data_item(self):
        main_window = QMainWindow()
        data_item = QListWidgetItem()
        data_item.setSizeHint(main_window.sizeHint())
        return data_item, main_window