from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QHeaderView
from widget_utils import AnvnDockWidget, AnvnOpButton
from PyQt5.QtCore import Qt
from widget_utils import AnvnComboBox

class AnvnTableWidget(QTableWidget):
    def __init__(self):
        super(AnvnTableWidget, self).__init__()
        self.__init_style()
        self.model_ = self.selectionModel()

    def __init_style(self):
        self.setStyleSheet('''
            QTableWidget {
                border-style: none;
            }
            QHeaderView {
                border: 1px solid #dbdbdb;
            }
        ''')
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def get_selected(self):
        rows = self.model_.selectedRows()
        columns = self.model_.selectedColumns()
        return [r.row() for r in rows], [c.column() for c in columns]

    def remove_columns(self, columns):
        for c in columns:
            self.removeColumn(c)

    def remove_rows(self, rows):
        for r in rows:
            self.removeRow(r)


class AnvnModelOperationWidget(AnvnDockWidget):
    def __init__(self, title='Model Operation', parent=None):
        super(AnvnModelOperationWidget, self).__init__(title, parent)
        self.setStatusTip(title)
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.tokenizer = None
        self.data_choice = self.__get_data_choice()
        self.data_table_widget = AnvnTableWidget()
        # self.__add_data_table()
        self.__add_op_button()
        self.main_widget.setLayout(self.main_layout)
        self.setWidget(self.main_widget)
        self.outputs = None
        self.all_ots = None
        self.all_iis = None

    def init_tokenizer(self, tokenizer):
        self.tokenizer = tokenizer

    def injection_data(self, outputs: dict,  all_ots, all_iis):
        self.outputs = outputs
        self.all_ots = all_ots
        self.all_iis = all_iis
        o_keys = outputs.keys()
        keys_combo_box = AnvnComboBox()
        keys_combo_box.addItems(o_keys)
        self.data_choice.addWidget(keys_combo_box)

    def __get_data_choice(self):
        data_widget = QWidget()
        data_layout = QHBoxLayout()
        data_layout.addStretch(0)
        data_widget.setLayout(data_layout)
        self.main_layout.addWidget(data_widget)
        return data_layout

    # def __add_data_table(self):
    #     self.data_table_widget.setHorizontalHeaderLabels(
    #         ['id', '姓名', '年龄', '学号', '地址'])
    #     self.main_layout.addWidget(self.data_table_widget)

    def remove_func(self):
        rows, columns = self.data_table_widget.get_selected()
        self.data_table_widget.remove_columns(columns)
        self.data_table_widget.remove_rows(rows)

    def __add_op_button(self):
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.addStretch(0)
        AnvnOpButton('#d81e06', 'Remove', 'remove',
                     button_layout)(self.remove_func)

        button_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_widget)
