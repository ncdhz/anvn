from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QListWidget, QLabel, QListWidgetItem, QVBoxLayout
from PyQt5.QtCore import Qt
from widget_utils import AnvnDeleteButton, AnvnQDockWidget, AnvnOpButton

class AnvnSentenceInputWidget(AnvnQDockWidget):
    def __init__(self, title='Sentence Input', parent=None):
        super(AnvnSentenceInputWidget, self).__init__(title, parent)
        self.setStatusTip(title)
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.sent_list = QListWidget(self)
        self.sent_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sent_text_list = []
        self.sent_list.setStyleSheet('''
            QListWidget {border-style: none;}
        ''')
        self.main_layout.addWidget(self.sent_list)
        self.main_widget.setLayout(self.main_layout)
        self.setWidget(self.main_widget)
        self.add_item2list()
        self.__init_op_button()
    
    def __init_op_button(self):
        layout_widget = QWidget()

        layout = QHBoxLayout()
        layout.addStretch(0)

        AnvnOpButton('#d81e06', 'Clear', 'clear', layout)(self.clear_sent_func)
        AnvnOpButton('#eeb174', 'Add', 'add', layout)(self.add_sent_func)

        AnvnOpButton('#1296db', 'Run', 'run', layout)

        layout_widget.setLayout(layout)
        self.main_layout.addWidget(layout_widget)
    
    def clear_sent_func(self):
        self.sent_text_list = []
        self.sent_list.clear()
        self.add_item2list()

    def add_sent_func(self):
        self.add_item2list()

    def add_item2list(self):
        sent_item, sent_widget = self.__get_sent()
        self.sent_list.addItem(sent_item)
        self.sent_list.setItemWidget(sent_item, sent_widget)
    
    def delete_sent_func(self, index):
        def __delete_sent_func():
            self.sent_list.clear()
            del self.sent_text_list[index]
            for _ in self.sent_text_list:
                self.add_item2list()
        return __delete_sent_func

    def __get_sent(self):
        sent_widget = QWidget()
        sent_widget.setStyleSheet('''
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
        sent_v_layout = QVBoxLayout()

        sent_h_layout = QHBoxLayout()
        sent_index = self.sent_list.count()
        sent_label = QLabel(f'The {sent_index + 1}th sentence')
        sent_h_layout.addWidget(sent_label)

        sent_delete_button = AnvnDeleteButton(20, 20)(self.delete_sent_func(sent_index))
        sent_h_layout.addWidget(
            sent_delete_button, alignment=Qt.AlignmentFlag.AlignRight)

        sent_v_layout.addLayout(sent_h_layout)
        
        if len(self.sent_text_list) > sent_index:
            sent_text = self.sent_text_list[sent_index]
        else:
            sent_text = QTextEdit()
            self.sent_text_list.append(sent_text)

        sent_text.setFixedHeight(100)
        sent_v_layout.addWidget(sent_text)

        sent_widget.setLayout(sent_v_layout)
        sent_item = QListWidgetItem()
        sent_item.setSizeHint(sent_widget.sizeHint())
        return sent_item, sent_widget