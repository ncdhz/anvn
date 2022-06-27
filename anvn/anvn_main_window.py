from PyQt5.QtWidgets import QMainWindow, QStackedLayout, QWidget
from PyQt5.QtGui import QIcon
from anvn_resources import *
from anvn_menu_tool import AnvnToolBar, AnvnMenuBar
from anvn_page_widget import AnvnTabWidget
from anvn_select_model_widget import AnvnSelectModelWidget

class AnvnMainWindow(QMainWindow):
    def __init__(self) -> None:
        super(AnvnMainWindow, self).__init__()
        self.setMinimumSize(1200, 900)
        self.setWindowIcon(QIcon(':/logo'))
        self.menu_tool = {
            'File': [
                {
                    'name': 'Select Model',
                    'icon': ':/select_model',
                    'shortcut': 'Ctrl+M',
                    'tip': 'Select NLP pre training model',
                    'func':  self.__open_select_model_func
                },
            ],
        }
        self.__init_menu_tool_bar()
        main_widget = QWidget()
        self.main_layout = QStackedLayout()
        main_widget.setLayout(self.main_layout)

        self.tab_widget = AnvnTabWidget()
        self.tab_widget.tab_null.connect(self.__tab_null_func)
        self.main_layout.addWidget(self.tab_widget)

        self.select_model = AnvnSelectModelWidget()(self.__load_model_func)
        self.main_layout.addWidget(self.select_model)
        self.main_layout.setCurrentWidget(self.select_model)
        
        self.setCentralWidget(main_widget)
        self.status_bar_init()
    
    def __load_model_func(self, model_names, tokenizer_names):
        self.tab_widget.load_model(model_names, tokenizer_names, False)
        self.main_layout.setCurrentWidget(self.tab_widget)

    def __tab_null_func(self):
        self.main_layout.setCurrentWidget(self.select_model)
    
    def __open_select_model_func(self):
        self.main_layout.setCurrentWidget(self.tab_widget)
        select_model = AnvnSelectModelWidget()(self.tab_widget.load_model)
        self.tab_widget.addTab(select_model, 'Select Model')
        self.tab_widget.setCurrentWidget(select_model)

    def __init_menu_tool_bar(self):
        for mt in self.menu_tool:
            self.addToolBar(AnvnToolBar(mt, self.menu_tool[mt]))
        self.setMenuBar(AnvnMenuBar(self.menu_tool))

    def status_bar_init(self):
        self.statusBar().showMessage('Ready Go !!!')