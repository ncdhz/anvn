from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLineEdit, QFileDialog, QScrollArea
from anvn_widget_utils import AnvnLinkButton, AnvnInformationWidget, AnvnOpButton, AnvnFlowLayout, AnvnBadge
from anvn_utils import AnvnUtils
from PyQt5.QtCore import Qt, pyqtSignal

class AnvnSelectModelWidget(QFrame):

    clicked = pyqtSignal(list, list)

    def __call__(self, func):
        self.clicked.connect(func)
        return self

    def __init__(self, parent=None, error_message=None):
        super(AnvnSelectModelWidget, self).__init__(parent)
        self.spacing = 20
        self.tokenizer_names = []
        self.model_names = []
        self.setObjectName("select_model")
        self.setStatusTip('Select Model')
        
        self.main_layout = QVBoxLayout()
        self.model_base_names = [
            'bert-base-uncased', 'bert-base-cased', 'bert-large-uncased', 'bert-large-cased',
            'roberta-base', 'roberta-large',
            'xlnet-base-cased', 'xlnet-large-cased',
            'albert-base-v2', 'albert-large-v2', 'albert-xlarge-v2', 'albert-xxlarge-v2',
        ]
        self.set_error_message = self.__init_error_message(error_message)
        self.__init_base_model()
        self.__init_input_model()
        self.input_tokenizer = self.__init_input_tokenizer()
        self.__init_model_tokenizer_view()
        self.main_layout.addStretch(0)
        self.__set_style()
        self.setLayout(self.main_layout)
    
    def __init_error_message(self, error_message):
        information = AnvnInformationWidget('Error:', title_color='#d81e06')
        label = information.add_information(error_message, '#d81e06')
        self.main_layout.addWidget(information)
        self.main_layout.addSpacing(self.spacing)
        if error_message == None:
            information.hide()
        def set_label(text):
            if text is not None:
                label.setText(text)
                information.show()
            else:
                information.hide()
        
        return set_label


    def __set_style(self):
        self.setStyleSheet('''
            #select_model {
                background: #fff;
                padding: 0px 20px;
            }
        ''')
    
    def __add_model_tokenizer_func(self, name):
        self.tokenizer_names.append(name)
        self.model_names.append(name)
        self.__refresh_model_tokenizer_view()
    
    def __refresh_model_tokenizer_view(self):
        for i in range(self.main_layout.count() - 1, -1, -1):
            item = self.main_layout.itemAt(i)
            if  item.widget() is not self.input_tokenizer:
                self.main_layout.removeItem(item)
                if not item.spacerItem():
                    item.widget().deleteLater()
            else:
                break
        self.__init_model_tokenizer_view()
        self.main_layout.addStretch(0)

    def __init_base_model(self):
        information = AnvnInformationWidget('Select Model:')
        model_layout = AnvnFlowLayout()
        for model_name in self.model_base_names:
            model_layout.addWidget(AnvnLinkButton(model_name)(self.__add_model_tokenizer_func))
            model_layout.addSpacing(self.spacing)
        information.add_layout(model_layout)
        self.main_layout.addWidget(information)

    def __model_text_changed_func(self, add):
        def mtc(text):
            if len(text) > 0:
                add.setDisabled(False)
            else:
                add.setDisabled(True)
        return mtc

    def __init_model_tokenizer(self, title, is_file, func=None):
        def add_model_tokenizer(mn):
            def amt():
                if func is not None:
                    func(mn.text())
                    mn.clear()
            return amt

        def choice_file_folder(mn):
            def cff():
                if not is_file:
                    src_path = QFileDialog.getExistingDirectory(None, 'Select file or folder', '/')
                else:
                    src_path = QFileDialog.getOpenFileName(None, 'Select file', '/')[0]
                mn.setText(src_path)
            return cff

        self.main_layout.addSpacing(self.spacing)
        information = AnvnInformationWidget(title)
        layout = QHBoxLayout()
        model_name = QLineEdit()
        model_name.setStyleSheet('''
            QLineEdit {
                border: 1px solid #dbdbdb;
                border-radius: 5px;
                padding: 5px 5px 6px 5px;
            }
        ''')
        layout.addWidget(model_name)
        file_folder = AnvnOpButton(icon_name='folder')(choice_file_folder(model_name))
        layout.addWidget(file_folder)
        add = AnvnOpButton('#17abe3', 'Add', 'madd')(add_model_tokenizer(model_name))
        add.setDisabled(True)
        layout.addWidget(add)
        model_name.textChanged.connect(self.__model_text_changed_func(add))
        information.add_layout(layout)
        self.main_layout.addWidget(information)
        return information

    def __add_tokenizer_func(self, name):
        self.tokenizer_names.append(name)
        self.__refresh_model_tokenizer_view()

    def __add_model_func(self, name):
        self.model_names.append(name)
        self.__refresh_model_tokenizer_view()

    def __init_input_tokenizer(self):
        return self.__init_model_tokenizer('Input Tokenizer Name:', False, self.__add_tokenizer_func)

    def __init_input_model(self):
        self.__init_model_tokenizer('Input Model Name:', True, self.__add_model_func)

    def __delete_model_tokenizer_name_func(self, names, index):
        def dmtn():
            names.pop(index)
            self.__refresh_model_tokenizer_view()
        return dmtn

    def __get_names_badge(self, names):
        names_frame = QFrame()
        names_frame.setObjectName('names_frame')
        scroll = QScrollArea()
        layout = AnvnFlowLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        for i, name in enumerate(names):
            layout.addWidget(AnvnBadge(AnvnUtils.middle_text_omission(name, 20))(self.__delete_model_tokenizer_name_func(names, i)))
            layout.addSpacing(5)
        if len(names) == 0:
            layout.addWidget(AnvnBadge('null', close=False))
        names_frame.setLayout(layout)
        scroll.setWidget(names_frame)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('''
            QScrollArea {
                border: none;
                background: #fff;
            }
            #names_frame {
                background: #fff;
            }
        ''')
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        return scroll

    def __init_model_tokenizer_view(self):
        self.main_layout.addSpacing(self.spacing)
        model_tokenizer_names = AnvnInformationWidget('Model Names:')
        model_names = self.__get_names_badge(self.model_names)
        model_tokenizer_names.add_widget(model_names)
        model_tokenizer_names.add_title('Tokenizer Names:')
        tokenizer_names = self.__get_names_badge(self.tokenizer_names)
        model_tokenizer_names.add_widget(tokenizer_names)
        but_layout = QHBoxLayout()
        but_layout.addStretch(0)

        clear = AnvnOpButton('#d81e06', 'Clear', 'clear', but_layout)(self.__clear_data_func)
        submit = AnvnOpButton('#17abe3', 'Submit', 'run', but_layout)(lambda: self.clicked.emit(self.model_names, self.tokenizer_names))
        if len(self.tokenizer_names) != 0 and len(self.tokenizer_names) == len(self.model_names):
            self.set_error_message(None)
        else:
            if len(self.tokenizer_names) > len(self.model_names):
                self.set_error_message('More tokenizer names than model names.')
            elif len(self.tokenizer_names) < len(self.model_names):
                self.set_error_message('Less tokenizer names than model names.')
            else:
                self.set_error_message(None)
            submit.setDisabled(True)
        
        if len(self.model_names) != 0 or len(self.tokenizer_names) != 0:
            clear.setDisabled(False)
        else:
            clear.setDisabled(True)

        model_tokenizer_names.add_layout(but_layout)
        self.main_layout.addWidget(model_tokenizer_names)
        self.main_layout.addSpacing(self.spacing)

    def __clear_data_func(self):
        self.tokenizer_names = []
        self.model_names = []
        self.__refresh_model_tokenizer_view()