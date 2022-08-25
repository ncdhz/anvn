from anvn_widget_utils import AnvnDockWidget
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from anvn_chart_management import AnvnLastHiddenStateChartManagement, AnvnPoolerChartManagement, AnvnHiddenStatesChartManagement, AnvnAttentionsChartManagement
from anvn_data import AnvnVisualData

class AnvnDataVisualizationWidget(AnvnDockWidget):

    handle = pyqtSignal()

    def __init__(self, config, title='Data Visualization'):
        super(AnvnDataVisualizationWidget, self).__init__(title)
        self.setStatusTip(title)
        self.data_list = QListWidget(self)
        self.data_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.data_list.setStyleSheet('''
            QListWidget {
                border: 1px solid #e0e0e0;
                margin: 0px 10px 10px 10px;
            }
            QListWidget::item {
                border-style: none;
            }
        ''')
        self.config = config
        self.data_visualization_list = []
        self.setMinimumWidth(500)
        self.setWidget(self.data_list)

    def data_monitor(self, table_data: AnvnVisualData):
        self.add_data(table_data)

    def add_data(self, data):
        self.__add_data_item(data)

    def __add_data_item(self, data):
        data_item, widget, data_widget = self.__get_data_item(data)
        self.data_list.addItem(data_item)
        self.data_list.setItemWidget(data_item, widget)
        if data is not None:
            self.__choice_node_func(data_widget)
    
    def __choice_node_func(self, node):
        for data_widget in self.data_visualization_list:
            if data_widget is node:
                data_widget.open()
            else:    
                data_widget.clear()

    def __close_chart_func(self, index):
        def cc():
            self.data_list.clear()
            del self.data_visualization_list[index]
            for _ in self.data_visualization_list:
                self.__add_data_item(None)
            if len(self.data_visualization_list) > 0:
                self.__choice_node_func(self.data_visualization_list[0])
            else:
                self.handle.emit()

        return cc

    def __get_data_item(self, data):
        
        index = self.data_list.count()
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        if data is not None:
            title = f'{data.get_key()}:{index + 1}'
            if data.get_key() == self.last_hidden_state:
                data_widget = AnvnLastHiddenStateChartManagement(data, title=title)
            elif data.get_key() == self.pooler_output:
                data_widget = AnvnPoolerChartManagement(data, title=title)
            elif data.get_key() == self.hidden_states:
                data_widget = AnvnHiddenStatesChartManagement(data, title=title)
            elif data.get_key() == self.attentions:
                data_widget = AnvnAttentionsChartManagement(data, title=title)
        else:
            data_widget = self.data_visualization_list[index]
            title = f'{data_widget.get_key()}:{index + 1}'
            data_widget.set_title(title)

        
        data_widget.set_title_double_clicked(self.__choice_node_func)
        data_widget.reduction_event(self.__choice_node_func)
        data_widget.floating_event(self.__choice_node_func)
        data_widget.set_close(self.__close_chart_func(index))
        layout.addWidget(data_widget)
        widget.setLayout(layout)
        data_item = QListWidgetItem()
        if data is not None:
            self.data_visualization_list.append(data_widget)
        else:
            self.data_visualization_list[index] = data_widget
        data_widget.set_list_item(data_item)
        data_item.setSizeHint(widget.sizeHint())
        return data_item, widget, data_widget

