from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget
from widget_utils import AnvnQDockWidget

class AnvnModelOperationWidget(AnvnQDockWidget):
    def __init__(self, title='Model Operation', parent=None):
        super(AnvnModelOperationWidget, self).__init__(title, parent)
        self.setStatusTip(title)
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.__add_data_choice()
        self.__add_data_table()
        self.__add_op_button()

        self.main_widget.setLayout(self.main_layout)
        self.setWidget(self.main_widget)
    
    def __add_data_choice(self):
        data_widget = QWidget()
        data_layout = QHBoxLayout()
        data_b = QPushButton()
        data_layout.addWidget(data_b)
        data_widget.setLayout(data_layout)
        self.main_layout.addWidget(data_widget)

    def __add_data_table(self):
        data_table_widget = QTableWidget()
        data_table_widget.setHorizontalHeaderLabels(['id','姓名','年龄','学号','地址'])

        self.main_layout.addWidget(data_table_widget)

    def __add_op_button(self):
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_b = QPushButton()
        button_layout.addWidget(button_b)

        button_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_widget)