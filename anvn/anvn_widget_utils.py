from PyQt5.QtWidgets import QDockWidget, QPushButton, QComboBox, QBoxLayout, QListView, QProgressBar, QDialog, QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QWidget, QStackedLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QEvent
from anvn_resources import *

class AnvnDockTitleBar(QFrame):
    def __init__(self, title, title_color='rgb(226, 192, 141)'):
        super(AnvnDockTitleBar, self).__init__()
        self.title_color = title_color
        self.title = title
        self.maximized_func = None
        self.reduction_func = None
        self.stacked_title = QStackedLayout()
        self.setLayout(self.stacked_title)

        self.only_title = self.__init_only_title()
        self.title_and_buttons = self.__init_title_and_buttons()
        self.stacked_title.setCurrentWidget(self.only_title)
        self.double_click_func = None
        self.__set_style()

    def __init_only_title(self):
        only_title = QWidget()
        title_label = QLabel(self.title)
        only_title_layout = QHBoxLayout()
        only_title_layout.addWidget(title_label)
        only_title.setLayout(only_title_layout)
        only_title_layout.setContentsMargins(0, 0, 0, 0)
        self.stacked_title.addWidget(only_title)
        return only_title
    
    def set_double_click_func(self, func):
        self.double_click_func = func

    def mouseDoubleClickEvent(self, a0):
        if self.double_click_func is not None:
            self.double_click_func()

    def __maximized_func(self, maximize_recovery):
        def __mf():
            if self.maximized_func is not None:
                self.maximized_func(maximize_recovery)
        return __mf

    def set_maximized_func(self, func):
        self.maximized_func = func
    
    def set_reduction_func(self, func):
        self.reduction_func = func

    def __reduction_func(self):
        if self.reduction_func is not None:
            self.reduction_func()

    def __init_title_and_buttons(self):
        title_and_buttons = QWidget()
        title_and_buttons_layout = QHBoxLayout()
        title_label = QLabel(self.title)
        title_and_buttons_layout.addWidget(title_label)
        title_and_buttons_layout.addStretch(0)
        maximize_recovery = AnvnMaximizeRecoveryButton()
        maximize_recovery(self.__maximized_func(maximize_recovery))
        title_and_buttons_layout.addWidget(maximize_recovery)
        reduction = AnvnDeleteButton()(self.__reduction_func)
        title_and_buttons_layout.addWidget(reduction)
        title_and_buttons.setLayout(title_and_buttons_layout)
        self.stacked_title.addWidget(title_and_buttons)
        title_and_buttons_layout.setContentsMargins(0, 0, 0, 0)
        return title_and_buttons

    def choice_only_title(self):
        self.stacked_title.setCurrentWidget(self.only_title)
    
    def choice_title_and_buttons(self):
        self.stacked_title.setCurrentWidget(self.title_and_buttons)

    def __set_style(self):
        self.setStyleSheet('''
            QFrame {
                padding: 0px 5px;
            }
            QLabel {
                color: ''' + self.title_color + ''';
            }
        ''')

class AnvnDockWidget(QDockWidget):
    def __init__(self, title='', parent=None, title_color='rgb(226, 192, 141)'):
        super(AnvnDockWidget, self).__init__(title, parent)
        self.setStyleSheet('''
            QDockWidget {
                background-color: #fff;
            }
        ''')
        self.is_floating = False
        self.title_bar = AnvnDockTitleBar(title, title_color)
        self.title_bar.set_maximized_func(self.__maximized_func)
        self.title_bar.set_reduction_func(self.__reduction_func)

        self.setTitleBarWidget(self.title_bar)

    def moveEvent(self, a0):
        super().moveEvent(a0)
        if self.isFloating() != self.is_floating:
            if self.isFloating():
                self.title_bar.choice_title_and_buttons()
            else:
                self.title_bar.choice_only_title()
            self.is_floating = self.isFloating()
    
    def set_title_double_clicked(self, func):
        self.title_bar.set_double_click_func(func)

    def __reduction_func(self):
        self.setFloating(False)

    def __maximized_func(self, button):
        if self.isMaximized():
            self.showNormal()
            button.show_maximize()
        else:
            self.showMaximized()
            button.show_recovery()

class AnvnButton(QPushButton):
    def __init__(self):
        super(AnvnButton, self).__init__()

    def __call__(self, callback):
        self.clicked.connect(callback)
        return self

class AnvnIconChangeButton(AnvnButton):
    def __init__(self, width=20, height=20, icon_leave=None, icon_enter=None):
        super().__init__()
        self.icon_enter = QIcon(icon_enter)
        self.icon_leave = QIcon(icon_leave)
        self.setIconSize(QSize(width, height))
        self.setIcon(self.icon_leave)
        self.__set_style()

    def __set_style(self):
        self.setStyleSheet('''
            QPushButton {
                border: none;
                margin: 8px;
                padding: 0px;
            }
        ''')
    
    def set_icon_enter(self, icon_enter):
        self.icon_enter = QIcon(icon_enter)
    
    def set_icon_leave(self, icon_leave):
        self.icon_leave = QIcon(icon_leave)

    def enterEvent(self, a0: QEvent) -> None:
        self.setIcon(self.icon_enter)
        return super().enterEvent(a0)

    def leaveEvent(self, a0: QEvent) -> None:
        self.setIcon(self.icon_leave)
        return super().leaveEvent(a0)

class AnvnDeleteButton(AnvnIconChangeButton):
    def __init__(self, w=20, h=20,):
        super(AnvnDeleteButton, self).__init__(width=w, height=h, icon_leave=':/delete', icon_enter=':/delete_cover')

class AnvnMaximizeRecoveryButton(AnvnIconChangeButton):
    def __init__(self, width=20, height=20):
        super().__init__(width, height, icon_leave=':/maximize', icon_enter=':/maximize_cover')
    
    def show_maximize(self):
        self.set_icon_enter(':/maximize_cover')
        self.set_icon_leave(':/maximize')
        self.setIcon(self.icon_leave)

    def show_recovery(self):
        self.set_icon_enter(':/recovery_cover')
        self.set_icon_leave(':/recovery')
        self.setIcon(self.icon_leave)

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
                border-radius: 5px;
                padding: 5px 10px;
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

    def __set_style(self, disabled=False):
        self.setStyleSheet('''
            QComboBox {
                background: #ffffff;
                border: 1px solid #dbdbdb;
                border-radius: 5px;
                padding: 5px 0px 5px 15px;
                color: ''' + ('''#17abe3''' if not disabled else '''rgb(219, 219, 219)''') + ''';
                height: 20px;
            }
            QComboBox::drop-down {
                border-style: none;
                width:40px;
            }
            QComboBox::down-arrow {
                image: ''' + ('''url(:/drop_down)''' if not disabled else '''url(:/drop_down_disabled)''') + ''';
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

    def setDisabled(self, a0: bool) -> None:
        self.__set_style(a0)
        super().setDisabled(a0)

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
        self.setWindowFlags(
            Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.Dialog)
        self.setWindowIcon(QIcon(':/logo'))


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
                background: #f7f7f9;
                padding: 10px;
                border-radius: 0px 0px 6px 6px;
            }
            QHeaderView {
                background: #f7f7f9;
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
        rows = [r.row() for r in rows]
        columns = [c.column() for c in columns]
        return sorted(rows), sorted(columns)

    def data2table(self, data, horizontal_header, vertical_header, digit=5):
        self.clear()
        self.setRowCount(len(vertical_header))
        self.setColumnCount(len(horizontal_header))
        self.setHorizontalHeaderLabels(horizontal_header)
        self.setVerticalHeaderLabels(vertical_header)
        for i in range(len(data)):
            for j in range(len(data[i])):
                twi = QTableWidgetItem(str(round(data[i][j], digit)))
                twi.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(i, j, twi)
