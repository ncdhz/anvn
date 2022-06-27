from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QTextEdit, QListWidget, QLabel, QListWidgetItem, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
import json
from anvn_widget_utils import AnvnCloseButton, AnvnDockWidget, AnvnOpButton

class AnvnDataInputWidget(AnvnDockWidget):

    handle = pyqtSignal(list)

    def __init__(self, title='Data Input', parent=None):
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
        self.add_item2list()
        self.main_layout.addWidget(self.data_list)
        self.run = self.__init_op_button()
        self.main_widget.setLayout(self.main_layout)
        self.setWidget(self.main_widget)

    def __run_func(self):
        data_list = []
        for dtl in self.data_text_list:
            dl = dtl.toPlainText()
            try:
                dl = json.loads(dl)
            except:
                pass
            
            if type(dl) != list:
                dl = [str(dl)]
            else:
                dl = [str(d) for d in dl]
            data_list.append(dl)

        self.handle.emit(data_list)

    def set_run_disabled(self, disabled, tool_tip=''):
        self.run.setToolTip(tool_tip)
        self.run.setDisabled(disabled)

    def __init_op_button(self):
        layout_widget = QWidget()

        layout = QHBoxLayout()
        layout.addStretch(0)
        AnvnOpButton('#d81e06', 'Clear', 'clear', layout)(self.__clear_data_func)
        AnvnOpButton('#eeb174', 'Add', 'add', layout)(self.__add_data_func)
        run = AnvnOpButton('#1296db', 'Run', 'run', layout)(self.__run_func)
        
        layout_widget.setLayout(layout)
        self.main_layout.addWidget(layout_widget)
        return run 
    
    def __clear_data_func(self):
        self.data_text_list = []
        self.data_list.clear()
        self.add_item2list()

    def __add_data_func(self):
        self.add_item2list()

    def add_item2list(self):
        data_item, data_widget = self.__get_data()
        self.data_list.addItem(data_item)
        self.data_list.setItemWidget(data_item, data_widget)
    
    def __delete_data_func(self, index):
        def dd():
            self.data_list.clear()
            del self.data_text_list[index]
            for _ in self.data_text_list:
                self.add_item2list()
        return dd

    def __get_data(self):
        data_widget = QFrame()
        data_widget.setStyleSheet('''
            QFrame {
                background-color: #fff;
            }
            QFrame QLabel {
                color: #1296db;
                margin: 0px 8px 8px 8px;
            }
            QTextEdit {
                border: 1px solid #e6e6e6;
                border-radius: 5px;
                margin: 0px 8px 2px 8px;
                padding: 5px;
            }
        ''')
        data_v_layout = QVBoxLayout()

        data_h_layout = QHBoxLayout()
        data_index = self.data_list.count()
        data_label = QLabel(f'Article {data_index + 1} data:')
        data_h_layout.addWidget(data_label)

        data_delete_button = AnvnCloseButton(20, 20)(self.__delete_data_func(data_index))
        data_h_layout.addWidget(
            data_delete_button, alignment=Qt.AlignmentFlag.AlignRight)

        data_v_layout.addLayout(data_h_layout)
        
        if len(self.data_text_list) > data_index:
            data_text = self.data_text_list[data_index]
        else:
            data_text = QTextEdit()
            data_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.data_text_list.append(data_text)
            data_text.setFixedHeight(70)
        data_v_layout.addWidget(data_text)

        data_widget.setLayout(data_v_layout)
        data_item = QListWidgetItem()
        data_item.setSizeHint(data_widget.sizeHint())
        return data_item, data_widget