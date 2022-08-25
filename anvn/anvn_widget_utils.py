from PyQt5.QtWidgets import QDockWidget, QPushButton, QComboBox, QBoxLayout, QListView, QProgressBar, QDialog, QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QWidget, QStackedLayout, QHBoxLayout, QHeaderView, QLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QEvent, pyqtSignal, QRect, QPoint
from anvn_resources import *
from anvn_data import AnvnVisualData

class AnvnDockTitleBar(QFrame):
    def __init__(self, title, color='rgb(226, 192, 141)', background=None):
        super(AnvnDockTitleBar, self).__init__()
        self.color = color
        self.maximized_func = None
        self.reduction_func = None
        self.stacked_title = QStackedLayout()
        self.background = background
        self.setLayout(self.stacked_title)
        self.only_title_label = QLabel(title)
        self.title_and_buttons_label = QLabel(title)
        self.only_title = self.__init_only_title()
        self.title_and_buttons = self.__init_title_and_buttons()
        self.stacked_title.setCurrentWidget(self.only_title)
        self.double_click_func = None
        self.__set_style()

    def __init_only_title(self):
        only_title = QWidget()
        only_title_layout = QHBoxLayout()
        only_title_layout.addWidget(self.only_title_label)
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
        if self.maximized_func is not None:
            self.maximized_func(maximize_recovery)

    def set_maximized_func(self, func):
        self.maximized_func = func
    
    def set_reduction_func(self, func):
        self.reduction_func = func

    def set_title(self, title):
        self.only_title_label.setText(title)
        self.title_and_buttons_label.setText(title)

    def __reduction_func(self, maximize_recovery, reduction):
        reduction.leave()
        if self.reduction_func is not None:
            self.reduction_func(maximize_recovery)

    def __init_title_and_buttons(self):
        title_and_buttons = QWidget()
        title_and_buttons_layout = QHBoxLayout()
        title_and_buttons_layout.addWidget(self.title_and_buttons_label)
        title_and_buttons_layout.addStretch(0)
        maximize_recovery = AnvnMaximizeRecoveryButton()
        maximize_recovery(lambda: self.__maximized_func(maximize_recovery))
        title_and_buttons_layout.addWidget(maximize_recovery)
        reduction = AnvnCloseButton()
        reduction(lambda: self.__reduction_func(maximize_recovery, reduction))
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
        frame_style = ''' 
            QFrame {
                padding: 8px 5px;
            }
        '''
        if self.background is not None:
            frame_style = '''
                QFrame {
                    padding: 8px 5px;
                    background:'''+ self.background +''';
                }
            '''

        label_style = '''    
            QLabel {
                color: ''' + self.color + ''';
            }
        '''

        self.setStyleSheet(frame_style + label_style)

class AnvnDockWidget(QDockWidget):
    def __init__(self, title='', parent=None, title_color='rgb(226, 192, 141)', title_background = None):
        super(AnvnDockWidget, self).__init__(title, parent)
        self.setStyleSheet('''
            QDockWidget {
                background-color: #fff;
            }
        ''')
        self.is_floating = False
        self.title_bar = AnvnDockTitleBar(title, title_color, title_background)
        self.title_bar.set_maximized_func(self.__maximized_func)
        self.title_bar.set_reduction_func(self.__reduction_func)
        self.reduction_func = None
        self.floating_func = None
        self.setTitleBarWidget(self.title_bar)

    def moveEvent(self, a0):
        super().moveEvent(a0)
        self.__title_bar_choice()

    def __title_bar_choice(self):
        if self.isFloating() != self.is_floating:
            if self.isFloating():
                self.title_bar.choice_title_and_buttons()
                if self.floating_func is not None:
                    self.floating_func()
            else:
                self.title_bar.choice_only_title()
            self.is_floating = self.isFloating()

    def set_title(self, title):
        self.title_bar.set_title(title)
    
    def set_floating_func(self, func):
        self.floating_func = func
    
    def set_title_double_clicked(self, func):
        self.title_bar.set_double_click_func(func)

    def set_reduction_func(self, func):
        self.reduction_func = func

    def __reduction_func(self, button):
        self.setFloating(False)
        button.show_maximize()
        self.__title_bar_choice()

        if self.reduction_func is not None:
            self.reduction_func()
    
    def __maximized_func(self, button):
        if self.isMaximized():
            self.showNormal()
            button.show_maximize()
        else:
            self.showMaximized()
            button.show_recovery()

class AnvnButton(QPushButton):

    def __init__(self, text=''):
        super(AnvnButton, self).__init__(text)

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
                margin: 0px;
                padding: 0px;
            }
        ''')
    
    def set_icon_enter(self, icon_enter):
        self.icon_enter = QIcon(icon_enter)
    
    def set_icon_leave(self, icon_leave):
        self.icon_leave = QIcon(icon_leave)

    def enterEvent(self, a0: QEvent) -> None:
        self.enter()
        return super().enterEvent(a0)

    def enter(self):
        self.setIcon(self.icon_enter)

    def leaveEvent(self, a0: QEvent) -> None:
        self.leave()
        return super().leaveEvent(a0)

    def leave(self):
        self.setIcon(self.icon_leave)

class AnvnCloseButton(AnvnIconChangeButton):
    def __init__(self, w=20, h=20,):
        super(AnvnCloseButton, self).__init__(width=w, height=h, icon_leave=':/close', icon_enter=':/close_cover')

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
    def __init__(self, color='#17abe3', text='', icon_name=None, layout: QBoxLayout=None, w=25, h=25, spacing=5, alignment=Qt.AlignmentFlag.AlignRight):
        super(AnvnOpButton, self).__init__()
        self.__set_style(color)
        self.color = color
        self.setText(text)
        if icon_name is not None:
            self.setIcon(QIcon(f':/{icon_name}'))
        self.setIconSize(QSize(w, h))
        if layout is not None:
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
                padding: 3px 10px;
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
    def __init__(self, layout: QBoxLayout=None, alignment=Qt.AlignmentFlag.AlignLeft, spacing=20) -> None:
        super().__init__()
        self.__set_style()
        self.setView(QListView())
        if layout is not None:
            layout.addWidget(self, alignment=alignment)
            if alignment == Qt.AlignmentFlag.AlignRight:
                layout.addSpacing(spacing)
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
                image: ''' + ('''url(:/down)''' if not disabled else '''url(:/down_disabled)''') + ''';
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
    def __init__(self, color, layout: QBoxLayout=None, minimum=0, maximum=100, alignment=Qt.AlignmentFlag.AlignTop) -> None:
        super(AnvnProgressBar, self).__init__()
        self.color = color
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.__set_style()
        if layout is not None:
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
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 15px;
            }
        ''')


class AnvnInformationWidget(AnvnFrame):
    def __init__(self, title, title_color='#17abe3', spacing=5) -> None:
        super().__init__()
        self.spacing = spacing
        self.title_color = title_color
        self.main_layout = QVBoxLayout()
        self.title = QLabel(title)
        self.title.setWordWrap(True)
        self.main_layout.addWidget(self.title)
        self.setLayout(self.main_layout)
        self.__set_style()

    def __set_style(self):
        self.__set_title_style(self.title)

    def __set_title_style(self, title):
        title.setStyleSheet('''
            QLabel {
                font-weight: bold;
                color: ''' + self.title_color + ''';
            }
        ''')

    def add_widget(self, widget):
        self.main_layout.addSpacing(self.spacing)
        self.main_layout.addWidget(widget)
        return self
    
    def add_layout(self, layout):
        self.main_layout.addSpacing(self.spacing)
        self.main_layout.addLayout(layout)
        return self

    def add_stretch(self, stretch):
        self.main_layout.addStretch(stretch)

    def add_title(self, title):
        self.main_layout.addSpacing(self.spacing)
        title_label = QLabel(title)
        self.main_layout.addWidget(title_label)
        self.__set_title_style(title_label)

    def add_information(self, information, color='#8a8a8a'):
        self.main_layout.addSpacing(self.spacing)
        label = QLabel(information)
        label.setWordWrap(True)
        self.main_layout.addWidget(label)
        label.setStyleSheet(f'color: {color}')
        return label


class AnvnTableWidget(QTableWidget):
    def __init__(self, data, horizontal_headers, vertical_headers, key):
        super(AnvnTableWidget, self).__init__()
        self.__set_style()
        self.model_ = self.selectionModel()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.data = AnvnVisualData(data, horizontal_headers, vertical_headers, key)
        self.digit = None

    def get_digit(self):
        return self.digit

    def get_data(self):
        return self.data

    def __set_style(self):
        self.setStyleSheet('''
            QTableWidget {
                border-style: none;
                border-radius: 0px 0px 6px 6px;
                gridline-color : #fff;
            }
            QHeaderView {
                background: #ffffff;
            }
            QHeaderView::section {
                border-style: none;
                background: #dedfe1;
            }

            QTableWidget::item::selected {
                background: #cccccc;
            }

            QScrollBar:horizontal{
                height:8px;  
                border-style:flat;
                border:0px;
                height:12px; 
            } 
            QScrollBar::handle:horizontal{
                min-width:91px; 
                background: #dedfe1;
                border-style:flat;
            }
            QScrollBar::handle:horizontal::hover{ 
                background: #c8c9cc;
            }
            QScrollBar::handle:horizontal::pressed{ 
                background: #c8c9cc;
            }
            QScrollBar::sub-page:horizontal {
                background: #fff;
                border-style:flat;
            }
            QScrollBar::add-page:horizontal {
                background: #fff;
                border-style:flat;
            }
            QScrollBar::sub-line:horizontal {
                background: #fff;
            }
            QScrollBar::add-line:horizontal{
                background: #fff;
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

    def data2table(self, data_op=None, horizontal_headers_op=None, vertical_headers_op=None, digit=5):
        if data_op is not None:
            self.data.set_data_op(data_op)
        
        if horizontal_headers_op is not None:
            self.data.set_horizontal_headers_op(horizontal_headers_op)
        
        if vertical_headers_op is not None:
            self.data.set_vertical_headers_op(vertical_headers_op)

        if digit != self.digit:
            self.digit = digit
        elif data_op is None and horizontal_headers_op is None and vertical_headers_op is None:
            return
        
        vertical_header = self.data.get_vertical_header()
        horizontal_header = self.data.get_horizontal_header()
        data = self.data.get_data()

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
        
class AnvnLinkButton(QLabel):
    
    clicked = pyqtSignal(str)

    def __init__(self, text):
        super(AnvnLinkButton, self).__init__()
        self.setText(text)
        self.__set_style()
        self.setFixedHeight(20)

    def __call__(self, func):
        self.clicked.connect(func)
        return self

    def mousePressEvent(self, ev):
        super().mousePressEvent(ev)
        self.clicked.emit(self.text())

    def __set_style(self):
        self.setStyleSheet('''
            QLabel {
                color: #87c38f;
                font-size: 18px;
                font-weight: bold;
                text-decoration: underline;
            }
            QLabel:hover {
                color: #bd2d30;
            }
        ''')

class AnvnBadge(QFrame):
    
    clicked = pyqtSignal()

    class AnvnBadgeCloseButton(AnvnIconChangeButton):
        def __init__(self, w=20, h=20):
            super().__init__(width=w, height=h, icon_leave=':/badge_close', icon_enter=':/close_cover')

    def __init__(self, text='', color='#87c38f', close=True, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName('badge')
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.text_label = QLabel(text)
        self.text_label.setFixedHeight(20)
        self.text_label.setObjectName('badge_text')
        layout.addWidget(self.text_label)
        if close:
            close_button = self.AnvnBadgeCloseButton()(self.__close_func)
            close_button.setObjectName('badge_close')
            layout.addWidget(close_button)
        self.setLayout(layout)
        self.__set_style(color=color)

    def __call__(self, func):
        self.clicked.connect(func)
        return self
        
    def __close_func(self):
        self.clicked.emit()

    def set_text(self, text):
        self.text_label.setText(text)

    def __set_style(self, color='#87c38f'):
        self.setStyleSheet('''
            #badge {
                background: #ffffff;
                border-radius: 5px;
                border: 1px solid #dbdbdb;
                padding: 5px 10px;
            }
            #badge_text {
                color: ''' + color + ''';
            }
        ''')
    
    def set_color(self, color):
        self.__set_style(color=color)

class AnvnFlowLayout(QLayout):
    heightChanged = pyqtSignal(int)

    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
            self.setSpacing(spacing)
        self.__item_list = []
    
    def __del__(self):
        while self.count():
            self.takeAt(0)
    
    def addItem(self, item):
        self.__item_list.append(item)

    def addSpacing(self, size): 
        self.addItem(QSpacerItem(size, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
    
    def count(self):
        return len(self.__item_list)
    
    def itemAt(self, index): 
        if 0 <= index and index < len(self.__item_list):
            return self.__item_list[index]
        return None
    
    def takeAt(self, index): 
        if 0 <= index and index < len(self.__item_list):
            return self.__item_list.pop(index)
        return None
    
    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))
    
    def hasHeightForWidth(self):
        return True
    
    def heightForWidth(self, width): 
        height = self.__do_layout(QRect(0, 0, width, 0), True)
        return height
    
    def setGeometry(self, rect): 
        super().setGeometry(rect)
        self.__do_layout(rect, False)
    
    def sizeHint(self): 
        return self.minimumSize()
    
    def minimumSize(self): 
        size = QSize()
    
        for item in self.__item_list:
            minsize = item.minimumSize()
            extent = item.geometry().bottomRight()
            size = size.expandedTo(QSize(minsize.width(), extent.y()))
    
        margin = self.contentsMargins().left()
        size += QSize(2 * margin, 2 * margin)
        return size
    
    def __do_layout(self, rect, test_only=False):
        m = self.contentsMargins()
        effective_rect = rect.adjusted(+m.left(), +m.top(), -m.right(), -m.bottom())
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0
    
        for item in self.__item_list:
            wid = item.widget()
    
            space_x = self.spacing()
            space_y = self.spacing()
            if wid is not None:
                space_x += wid.style().layoutSpacing(
                QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Horizontal)
                space_y += wid.style().layoutSpacing(
                QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Vertical)
        
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > effective_rect.right() and line_height > 0:
                x = effective_rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0
        
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
        
            x = next_x
            line_height = max(line_height, item.sizeHint().height())
    
        new_height = y + line_height - rect.y()
        self.heightChanged.emit(new_height)
        return new_height