from PyQt5.QtWidgets import QHBoxLayout, QDockWidget, QMainWindow, QPushButton
from PyQt5.QtGui import  QIcon
from PyQt5.QtCore import Qt, QSize, QEvent
from resources import *

class AnvnQDockWidget(QDockWidget):
    def __init__(self, title, parent=None):
        super(AnvnQDockWidget, self).__init__(title, parent)
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
        
    def enterEvent(self, a0: QEvent) -> None:
        self.setIcon(
            self.sent_delete_button_red_icon if not self.is_red else self.sent_delete_button_gray_icon)
        return super().enterEvent(a0)

    def leaveEvent(self, a0: QEvent) -> None:
        self.setIcon(
            self.sent_delete_button_red_icon if self.is_red else self.sent_delete_button_gray_icon)
        return super().leaveEvent(a0)

class AnvnOpButton(AnvnButton):
    def __init__(self, color, text, icon_name, layout: QHBoxLayout, w = 20, h = 20, spacing = 20, alignment=Qt.AlignmentFlag.AlignRight):
        super(AnvnOpButton, self).__init__()
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
        self.setText(text)
        self.setIcon(QIcon(f':/{icon_name}'))
        self.setIconSize(QSize(w, h))
        layout.addSpacing(spacing)
        layout.addWidget(self, alignment=alignment)

    