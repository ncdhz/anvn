from PyQt5.QtWidgets import QDockWidget, QPushButton, QComboBox, QBoxLayout, QListView, QProgressBar, QDialog, QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QEvent
from resources import *


class AnvnDockWidget(QDockWidget):
    def __init__(self, title, parent=None):
        super(AnvnDockWidget, self).__init__(title, parent)
        self.setStyleSheet('''
            QDockWidget {
                color: rgb(226, 192, 141);
            }
            QDockWidget::title {
                background: #ffffff;
                text-align: left center; 
            }
        ''')


class AnvnButton(QPushButton):
    def __init__(self):
        super(AnvnButton, self).__init__()

    def __call__(self, callback):
        self.clicked.connect(callback)
        return self


class AnvnDeleteButton(AnvnButton):
    def __init__(self, w, h, is_red=False):
        super(AnvnDeleteButton, self).__init__()
        self.is_red = is_red
        self.sent_delete_button_red_icon = QIcon(':/delete_red')
        self.sent_delete_button_gray_icon = QIcon(':/delete_gray')

        self.setIcon(
            self.sent_delete_button_red_icon if is_red else self.sent_delete_button_gray_icon)
        self.setIconSize(QSize(w, h))
        self.__set_style()
        
    def __set_style(self):
        self.setStyleSheet('''
            QPushButton {
                border: none;
                margin: 8px;
                padding: 0px;
            }
        ''')
        
    def enterEvent(self, a0: QEvent) -> None:
        self.setIcon(
            self.sent_delete_button_red_icon if not self.is_red else self.sent_delete_button_gray_icon)
        return super().enterEvent(a0)

    def leaveEvent(self, a0: QEvent) -> None:
        self.setIcon(
            self.sent_delete_button_red_icon if self.is_red else self.sent_delete_button_gray_icon)
        return super().leaveEvent(a0)

class AnvnOpButton(AnvnButton):
    def __init__(self, color, text, icon_name, layout: QBoxLayout, w=20, h=20, spacing=20, alignment=Qt.AlignmentFlag.AlignRight):
        super(AnvnOpButton, self).__init__()
        self.__set_style(color)
        self.color = color
        self.setText(text)
        self.setIcon(QIcon(f':/{icon_name}'))
        self.setIconSize(QSize(w, h))
        if alignment == Qt.AlignmentFlag.AlignRight:
            layout.addSpacing(spacing)
        layout.addWidget(self, alignment=alignment)
        if alignment != Qt.AlignmentFlag.AlignRight:
            layout.addSpacing(spacing)

    def __set_style(self, color):
        self.setStyleSheet('''
            QPushButton {
                background: #ffffff;
                border: 1px solid #dbdbdb;
                border-radius: 10px;
                padding: 5px 15px;
                color: ''' + color + ''';
            }
            QPushButton:hover {
                background: #e6e6e6;
            }
            QPushButton:pressed {
                background: #cdcdcd;
            }
        ''')

    def setDisabled(self, a0: bool):
        if a0:
            self.__set_style('rgb(219, 219, 219)')
        else:
            self.__set_style(self.color)
        super().setDisabled(a0)

class AnvnComboBox(QComboBox):
    def __init__(self, layout: QBoxLayout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=20) -> None:
        super().__init__()
        self.__set_style()
        layout.addWidget(self, alignment=alignment)
        if alignment == Qt.AlignmentFlag.AlignRight:
            layout.addSpacing(spacing)
        self.setView(QListView())
        if alignment != Qt.AlignmentFlag.AlignRight:
            layout.addSpacing(spacing)

    def __set_style(self):
        self.setStyleSheet('''
            QComboBox {
                background: #ffffff;
                border: 1px solid #dbdbdb;
                border-radius: 10px;
                padding: 5px 0px 5px 15px;
                color: #17abe3;
                height: 20px;
            }
            QComboBox::drop-down {
                border-style: none;
                width:40px;
            }
            QComboBox::down-arrow {
                image: url(:/drop_down);
                height:20px;
                width:20px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #dbdbdb;
            }
            QComboBox QAbstractItemView::item {
                height: 36px;
                color: rgb(51, 51, 51);
            }
        ''')

    def __call__(self, callback):
        self.currentTextChanged.connect(callback)
        return self

class AnvnProgressBar(QProgressBar):
    def __init__(self, layout: QBoxLayout, color, minimum=0, maximum=100, alignment=Qt.AlignmentFlag.AlignTop) -> None:
        super(AnvnProgressBar, self).__init__()
        self.color = color
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.__set_style()
        layout.addWidget(self, alignment=alignment)

    def __set_style(self):
        self.setStyleSheet('''
            QProgressBar {
                min-height: 12px;
                max-height: 12px;
                text-align: center;
                border-radius: 6px;
                font-size: 11px;
                border: 1px solid #dbdbdb;
                line-height: 12px;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background: ''' + self.color + ''';
            }
        ''')

class AnvnDialog(QDialog):
    def __init__(self, title, w=600, h=600, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(QSize(w, h))
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.Dialog)

class AnvnFrame(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName('anvn_frame')
        self.__set_style()

    def __set_style(self):
        self.setStyleSheet('''
            QFrame#anvn_frame {
                background: #ffffff;
                border: 1px solid #dbdbdb;
                border-radius: 10px;
                padding: 5px 15px;
            }
        ''')

class AnvnInformationWidget(AnvnFrame):
    def __init__(self, title) -> None:
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.title = QLabel(title)
        self.title.setWordWrap(True)
        self.main_layout.addWidget(self.title) 
        self.setLayout(self.main_layout)
        self.__set_style()

    def __set_style(self):
        self.title.setStyleSheet('''color: #17abe3;''')

    def add_widget(self, widget):
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(widget)
        return self
    
    def add_stretch(self, stretch):
        self.main_layout.addStretch(stretch)

    def add_information(self, information, color='#8a8a8a'):
        self.main_layout.addSpacing(10)
        label = QLabel(information)
        label.setWordWrap(True)
        self.main_layout.addWidget(label)
        label.setStyleSheet(f'color: {color}')
        return label

class AnvnTableWidget(QTableWidget):
    def __init__(self):
        super(AnvnTableWidget, self).__init__()
        self.__set_style()
        self.model_ = self.selectionModel()

    def __set_style(self):
        self.setStyleSheet('''
            QTableWidget {
                border-style: none;
            }
            QHeaderView {
                background: #ffffff;
            }
            QHeaderView::section {
                border: 1px solid #dbdbdb;
                background: #e6e6e6;
            }

        ''')
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

    def get_selected(self):
        rows = self.model_.selectedRows()
        columns = self.model_.selectedColumns()
        return [r.row() for r in rows], [c.column() for c in columns]

    def set_items(self, data, digit):
        for i in range(len(data)):
            for j in range(len(data[i])):
                twi = QTableWidgetItem(str(round(data[i][j], digit)))
                twi.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(i, j, twi)