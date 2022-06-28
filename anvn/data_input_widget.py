from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QListWidget, QLabel, QListWidgetItem, QVBoxLayout
from PyQt5.QtCore import Qt
from widget_utils import AnvnDeleteButton, AnvnDockWidget, AnvnOpButton

class AnvnDataInputWidget(AnvnDockWidget):
    def __init__(self, title='Data Input', callback_func=None, parent=None):
        super(AnvnDataInputWidget, self).__init__(title, parent)
        self.setStatusTip(title)
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.data_list = QListWidget(self)
        self.data_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.data_text_list = []
        self.data_list.setStyleSheet('''
            QListWidget {border-style: none;}
        ''')
        self.main_layout.addWidget(self.data_list)
        self.main_widget.setLayout(self.main_layout)
        self.setWidget(self.main_widget)
        self.add_item2list()
        op_layout = self.__init_op_button()
        self.run = AnvnOpButton('#1296db', 'Run', 'run', op_layout)(self.run_func)
        self.callback_func = callback_func

    def run_func(self):
        data_list = []
        for dtl in self.data_text_list:
            data_list.append(dtl.toPlainText())
        if self.callback_func is not None:
            self.callback_func(data_list)

    def set_run_disabled(self, disabled, tool_tip):
        self.run.setToolTip(tool_tip)
        self.run.setDisabled(disabled)

    def __init_op_button(self):
        layout_widget = QWidget()

        layout = QHBoxLayout()
        layout.addStretch(0)
        AnvnOpButton('#d81e06', 'Clear', 'clear', layout)(self.clear_data_func)
        AnvnOpButton('#eeb174', 'Add', 'add', layout)(self.add_data_func)
        layout_widget.setLayout(layout)
        self.main_layout.addWidget(layout_widget)
        return layout
    
    def clear_data_func(self):
        self.data_text_list = []
        self.data_list.clear()
        self.add_item2list()

    def add_data_func(self):
        self.add_item2list()

    def add_item2list(self):
        data_item, data_widget = self.__get_data()
        self.data_list.addItem(data_item)
        self.data_list.setItemWidget(data_item, data_widget)
    
    def delete_data_func(self, index):
        def __delete_data_func():
            self.data_list.clear()
            del self.data_text_list[index]
            for _ in self.data_text_list:
                self.add_item2list()
        return __delete_data_func

    def __get_data(self):
        data_widget = QWidget()
        data_widget.setStyleSheet('''
            QWidget {
                border-bottom: 1px solid #dbdbdb;
            }
            QLabel {
                color: #1296db;
                margin: 8px;
            }
            QTextEdit {
                border: 1px solid #e6e6e6;
                border-radius: 0px;
                margin: 0px 8px 15px 8px;
            }
            QPushButton {
                border: none;
                margin: 8px;
                padding: 0px;
            }
        ''')
        data_v_layout = QVBoxLayout()

        data_h_layout = QHBoxLayout()
        data_index = self.data_list.count()
        data_label = QLabel(f'Article {data_index + 1} data:')
        data_h_layout.addWidget(data_label)

        data_delete_button = AnvnDeleteButton(20, 20)(self.delete_data_func(data_index))
        data_h_layout.addWidget(
            data_delete_button, alignment=Qt.AlignmentFlag.AlignRight)

        data_v_layout.addLayout(data_h_layout)
        
        if len(self.data_text_list) > data_index:
            data_text = self.data_text_list[data_index]
        else:
            data_text = QTextEdit()
            self.data_text_list.append(data_text)

        data_text.setFixedHeight(100)
        data_v_layout.addWidget(data_text)

        data_widget.setLayout(data_v_layout)
        data_item = QListWidgetItem()
        data_item.setSizeHint(data_widget.sizeHint())
        return data_item, data_widget