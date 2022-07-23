from anvn_widget_utils import AnvnDockWidget
from anvn_table_management import AnvnTableManagement
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from anvn_chart_management import AnvnLastHiddenStateChartManagement, AnvnPoolerChartManagement, AnvnHiddenStatesChartManagement, AnvnAttentionsChartManagement
from anvn_data import AnvnData

class AnvnDataVisualizationWidget(AnvnDockWidget):
    def __init__(self, title='Data Visualization ', parent=None, last_hidden_state='last_hidden_state', pooler_output='pooler_output', hidden_states='hidden_states', attentions='attentions'):
        super(AnvnDataVisualizationWidget, self).__init__(title, parent)
        self.setStatusTip(title)
        self.data_list = QListWidget(self)
        self.data_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.data_list.setStyleSheet('''
            QListWidget {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                margin: 0px 10px 10px 10px;
            }
            QListWidget::item {
                border-style: none;
                border-radius: 5px;
            }
        ''')
        self.last_hidden_state = last_hidden_state
        self.pooler_output = pooler_output
        self.hidden_states = hidden_states
        self.attentions = attentions
        self.data_visualization_list = []
        self.setMinimumWidth(300)
        self.setWidget(self.data_list)

    def data_monitor(self, table: AnvnTableManagement):
        data = AnvnData(data=table.get_data(), data_num=table.get_data_num(), heads=table.get_heads(), layers=table.get_layers(), key=table.get_key(), horizontal_headers=table.get_horizontal_headers(), vertical_headers=table.get_vertical_headers(), horizontal_ids=table.get_horizontal_ids(), vertical_ids=table.get_vertical_ids())
        self.add_data(data)

    def add_data(self, data):
        self.__add_data_item(data)

    def __add_data_item(self, data):
        data_item, data_widget = self.__get_data_item(data)
        self.data_list.addItem(data_item)
        self.data_list.setItemWidget(data_item, data_widget)
    
    def __double_click_func(self, node):
        for dv in self.data_visualization_list:
            if dv is node:
                dv.open()
            else:    
                dv.clear()
        

    def __get_data_item(self, data):

        index = self.data_list.count()
        title = f'{data.get_key()}:{index + 1}'
        
        if data.get_key() == self.last_hidden_state:
            data_widget = AnvnLastHiddenStateChartManagement(data, title=title)
        elif data.get_key() == self.pooler_output:
            data_widget = AnvnPoolerChartManagement(data, title=title)
        elif data.get_key() == self.hidden_states:
            data_widget = AnvnHiddenStatesChartManagement(data, title=title)
        elif data.get_key() == self.attentions:
            data_widget = AnvnAttentionsChartManagement(data, title=title)
        
        data_widget.set_title_double_clicked(self.__double_click_func)
        self.data_visualization_list.append(data_widget)
        
        data_item = QListWidgetItem()

        data_item.setSizeHint(data_widget.sizeHint())
        return data_item, data_widget

