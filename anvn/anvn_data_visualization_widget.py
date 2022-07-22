from anvn_widget_utils import AnvnDockWidget
from anvn_table_management import AnvnTableManagement
from PyQt5.QtWidgets import QListWidget, QMainWindow, QListWidgetItem
from PyQt5.QtCore import Qt
from anvn_chart_management import AnvnChartManagement
from anvn_data import AnvnData

class AnvnDataVisualizationWidget(AnvnDockWidget):
    def __init__(self, title='Data Visualization ', parent=None):
        super(AnvnDataVisualizationWidget, self).__init__(title, parent)
        self.setStatusTip(title)
        self.data_list = QListWidget(self)
        self.data_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.data_visualization_list = []
        self.datas = []
        self.setWidget(self.data_list)
    
    def data_monitor(self, table: AnvnTableManagement):
        data = AnvnData(data=table.get_data(), data_num=table.get_data_num(), heads=table.get_heads(), layers=table.get_layers(), key=table.get_key(), horizontal_headers=table.get_horizontal_headers(), vertical_headers=table.get_vertical_headers(), horizontal_ids=table.get_horizontal_ids(), vertical_ids=table.get_vertical_ids())
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
        main_window.setMinimumHeight(200)
        main_window.setStyleSheet('''
            QMainWindow {background-color: #fafafa;}
        ''')
        index = self.data_list.count()
        data = self.datas[index]
        data_widget = AnvnChartManagement(data, title=f'{data.get_key()}:{index + 1}')
        main_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, data_widget)
        data_item = QListWidgetItem()
        data_item.setSizeHint(main_window.sizeHint())
        return data_item, main_window

