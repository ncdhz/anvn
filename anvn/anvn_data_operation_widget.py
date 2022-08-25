from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QStackedWidget, QListWidget, QListWidgetItem, QFrame
from anvn_widget_utils import AnvnDockWidget, AnvnOpButton, AnvnComboBox, AnvnProgressBar, AnvnDialog, AnvnInformationWidget, AnvnFrame
from PyQt5.QtCore import Qt, pyqtSignal
from anvn_utils import AnvnUtils
from anvn_table_management import AnvnTableManagement
from anvn_config import AnvnConfig
from anvn_data import AnvnBasicData, AnvnModelOutputData, AnvnVisualData
class AnvnDODialog(AnvnDialog):

    ok_handle = pyqtSignal(object)

    error = {
        1: 'Syntax error.',
        2: 'Array out of bounds.',
        3: 'Data is empty.'
    }
    
    def __init__(self, title, number, data):
        self.spacing = 10
        if type(data) is dict:
            dl = 3 if len(data) > 3 else len(data)
        else:
            dl = 1
        h = 200 + 3 * self.spacing + dl * (178 + self.spacing)

        super().__init__(title, h=h, w=700)
        
        self.setContentsMargins(10, 10, 10, 10)
        self.data = AnvnUtils.deepcopy(data)
        self.title = title
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.__set_help()
        self.ok, ok_frame = self.__init_op_button()
        self.input_list = QListWidget(self)
        self.input_list.setFixedHeight((178 + self.spacing) * dl - self.spacing)
        self.input_list.setStyleSheet('''
            QListWidget {
                border-style: none;
                background-color: rgba(0, 0, 0, 0);
            }
            QListWidget::item:hover {
                background-color: rgba(0, 0, 0, 0);
            }
        ''')
        self.input_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if type(number) is not dict:
            self.is_ok = True
            self.__add_input(number, None, True)
        else:
            self.is_ok = {}
            for i, (name, n) in enumerate(number.items()):
                self.__add_input(n, name, True if i == len(number) - 1 else False)
                self.is_ok[name] = True

        self.main_layout.addStretch(0)
        self.main_layout.addWidget(self.input_list)
        self.main_layout.addStretch(0)
        self.main_layout.addWidget(ok_frame)
        self.setLayout(self.main_layout)
        self.ok.setDisabled(True)

    def get_data(self):
        return self.data

    def __set_help(self):
        information = AnvnInformationWidget('Help:')
        self.main_layout.addWidget(information)
        information.add_information('Please enter a comma separated position [0-n] or use [i-j]. N represents the maximum value that can be selected, i represents the start position, and j represents the end position.', '#eeb174')

    def __set_ok_disabled(self):
        if type(self.is_ok) is dict:
            for _, is_ok in self.is_ok.items():
                if not is_ok:
                    self.ok.setDisabled(True)
                    return
            self.ok.setDisabled(False)
        elif self.is_ok:
            self.ok.setDisabled(False)
        else:
            self.ok.setDisabled(True)

    def __data_analysis(self, str_data, number):
        '''
        return: 1: error, 2: array out of bounds, 3: no data
        '''
        if str_data == '':
            return 3
        data = set()
        try:
            sds = str_data.split(',')
            for sd in sds:
                if '-' in sd:
                    s = sd.split('-')
                    if len(s) != 2:
                        return 1
                    for i in range(int(s[0]), int(s[1]) + 1):
                        if i >= number:
                            return 2
                        data.add(i)
                else:
                    if int(sd) >= number:
                        return 2
                    data.add(int(sd))
            pass
        except Exception:
            return 1
        if len(data) == 0:
            return 3

        data = list(data)
        data.sort()

        return data

    def __text_changed_func(self, lint_edit, text_edit, number, name=None):
        def tcf():
            data_analysis_result = self.__data_analysis(lint_edit.text(), number)
            if type(data_analysis_result) == list:
                result_text = ','.join(str(i) for i in data_analysis_result)
                text_edit.setStyleSheet('''
                    color: #8a8a8a;
                    border-style: none;
                ''')
                if name is not None:
                    self.data[name] = data_analysis_result
                    self.is_ok[name] = True
                else:
                    self.data = data_analysis_result
                    self.is_ok = True
            else:
                result_text = self.error[data_analysis_result]
                text_edit.setStyleSheet('''
                    color: #d81e06;
                    border-style: none;
                ''')
                if name is not None:
                    self.is_ok[name] = False
                    self.data[name] = []
                else:
                    self.is_ok = False
                    self.data = []

            text_edit.setText(result_text)
            
            self.__set_ok_disabled()
        return tcf

    def __add_input(self, number, name, is_end=False):
        input_frame = QFrame()
        input_frame.setProperty('class', 'input_frame')
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        information = AnvnInformationWidget(f'{self.title} [0, {number - 1}]{f"{name}" if name is not None else ""}:')
        lint_edit = QLineEdit()
        lint_edit.setStyleSheet('''
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 3px;
                color: #8a8a8a;
            }
        ''')
        information.add_widget(lint_edit)
        information.add_title('Result:')
        lint_edit.setPlaceholderText('e.g. 1,2,7-10,12')
        result_view = QTextEdit()
        result_view.setMaximumHeight(50)
        result_view.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        result_view.setReadOnly(True)
        information.add_widget(result_view)

        lint_edit.textChanged.connect(
            self.__text_changed_func(lint_edit, result_view, number, name))
            
        if name is not None:
            lint_edit.setText(AnvnUtils.list2str(',', self.data[name]))
        else:
            lint_edit.setText(AnvnUtils.list2str(',', self.data))
        
        input_layout.addWidget(information)
        information.setFixedHeight(178)
        input_frame.setLayout(input_layout)
        if not is_end:
            input_frame.setStyleSheet('''
                QFrame[class="input_frame"] {
                    padding-bottom: ''' + str(self.spacing) + '''px;
                }
            ''')
        
        item = QListWidgetItem()
        item.setSizeHint(input_frame.sizeHint())
        self.input_list.addItem(item)
        self.input_list.setItemWidget(item, input_frame)

    def __ok_func(self):
        self.ok_handle.emit(self.data)
        self.close()

    def __init_op_button(self):
        frame = AnvnFrame(self)
        layout = QHBoxLayout()
        layout.addStretch(0)
        ok = AnvnOpButton('#1296db', 'OK', 'ok', layout)(self.__ok_func)
        AnvnOpButton('#d81e06', 'Cancel', 'cancel', layout)(lambda: self.close())
        frame.setLayout(layout)
        return ok, frame

class AnvnLMOWidget(QWidget):

    def __init__(self) -> None:
        super(AnvnLMOWidget, self).__init__()
        self.main_layout = QVBoxLayout()
        self.set_error_message = self.__error_message()
        self.model_load_label, self.model_load_progress_bar = self.__model_load()
        self.data_load_label, self.data_load_progress_bar = self.__data_load()
        self.model_run_label, self.model_run_progress_bar = self.__model_run()
        self.show_button = self.__load_button()
        self.main_layout.addStretch(0)
        self.setLayout(self.main_layout)

    def __error_message(self):
        widget = QWidget()
        widget.setStyleSheet('''
            QWidget {
                margin: 0px 8px;
            }
            QWidget #error_title {
                padding-bottom: 5px;
                color: #d81e06;
                font-weight: bold;
            }
            QWidget #error_message {
                color: #d81e06;
            }
        ''')
        layout = QVBoxLayout()
        title_label = QLabel('Error:')
        title_label.setObjectName('error_title')
        layout.addWidget(title_label)
        message_label = QLabel('')
        message_label.setObjectName('error_message')
        layout.addWidget(message_label)
        widget.setLayout(layout)
        self.main_layout.addWidget(widget)
        widget.hide()

        def set_message(message=None):
            if message is None:
                message_label.clear()
                widget.hide()
            else:
                message_label.setText(message)
                widget.show()

        return set_message

    def __load_progress_bar(self, color, text, maximum):
        widget = QWidget()
        widget.setStyleSheet('''
            QWidget {
                margin: 0px 8px;
            }
            QWidget QLabel {
                color: ''' + color + ''';
                padding-bottom: 5px;
                font-weight: bold;
            }
        ''')
        layout = QVBoxLayout()
        label = QLabel(text)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignTop)
        progress_bar = AnvnProgressBar(
            color=color, maximum=maximum, layout=layout)
        layout.addStretch(0)
        widget.setLayout(layout)

        self.main_layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignTop)
        return label, progress_bar

    def __load_button(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.addStretch(0)
        button = AnvnOpButton('#1296db', 'Show', 'table', layout)
        button.setDisabled(True)
        widget.setLayout(layout)
        self.main_layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignTop)
        return button

    def clicked(self, callback_func):
        self.show_button(callback_func)

    def show_disabled(self, disabled):
        self.show_button.setDisabled(disabled)

    def __model_load(self):
        return self.__load_progress_bar('#8992c8', 'Wait for the model to load:', 0)

    def __data_load(self):
        return self.__load_progress_bar('#4f68b0', 'Waiting for data processing:', 100)

    def __model_run(self):
        return self.__load_progress_bar('#0061b0', 'Wait for the model to run:', 100)

    def set_model_load_text(self, text=None):
        if text == None:
            text = 'Wait for the model to load:'
        self.model_load_label.setText(text)

    def set_data_load_text(self, text=None):
        if text == None:
            text = 'Waiting for data processing:'
        self.data_load_label.setText(text)

    def set_model_run_text(self, text=None):
        if text == None:
            text = 'Wait for the model to run:'
        self.model_run_label.setText(text)

    def model_load_stop(self):
        self.model_load_progress_bar.setMaximum(100)
        self.model_load_progress_bar.setValue(100)

    def set_data_load_value(self, value):
        self.data_load_progress_bar.setValue(value)

    def set_model_run_value(self, value):
        self.model_run_progress_bar.setValue(value)

class AnvnMMOWidget(QWidget):

    handle = pyqtSignal(AnvnVisualData)

    def __init__(self, model_output: AnvnModelOutputData):
        super(AnvnMMOWidget, self).__init__()
        self.model_output = model_output
        self.config: AnvnConfig = model_output.get_config()

        self.basic_data = AnvnBasicData(model_tokenizer_names=[model_output.first_model_tokenizer_name()], key=self.config.model_output.attentions, decimal_digit=self.config.table.decimal_digit)
        

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.data_num_but, self.key_but, self.layer_but, self.head_but, self.digit_but, self.revoke_but, self.forward_but = self.__init_data_choice()
        self.main_layout.addSpacing(10)
        

        self.table_main = QStackedWidget()
        self.main_layout.addWidget(self.table_main)
        self.main_layout.addSpacing(10)
        self.__init_data_show()
        # add key connect, init table
        self.key_but(self.__key_changed_func)
        self.key_but.setCurrentText(self.config.model_output.attentions)
        self.__add_tabel_widget()
    
    def get_config(self):
        return self.config

    def __init_data_show(self):
        data_show = QHBoxLayout()
        data_show.addStretch(0)
        AnvnOpButton('#1296db', 'Show', 'show', data_show)(lambda: self.handle.emit(self.table_main.currentWidget().get_data()))
        self.main_layout.addLayout(data_show)

    def __add_tabel_widget(self):
        self.__remove_current_after_table()
        current_index = self.table_main.currentIndex()

        if current_index >= 0:
            tabel = self.table_main.currentWidget()
            tabel.remove_current_after_table()

        data = AnvnTableManagement.get_table_data(self.basic_data, self.model_output, self.config)
        table_mangement = AnvnTableManagement.get_table_management(data, self.basic_data.get_key(), self.config)
        table_mangement.handle.connect(self.__table_changed_func)
    
        self.table_main.addWidget(table_mangement)
        self.table_main.setCurrentWidget(table_mangement)

        self.__revoke_forward_disable()

    def __remove_current_after_table(self):
        for i in range(self.table_main.count() - 1, self.table_main.currentIndex(), -1):
            self.table_main.removeWidget(self.table_main.widget(i))
        

    def __table_changed_func(self):
        self.__remove_current_after_table()
        self.__revoke_forward_disable()

    def __do_dialog(self, name):
        def dd(data):
            is_op = False
            if name == self.config.dim_name.data_name and self.basic_data.get_data_num() != data:
                self.basic_data.set_data_num(data)
                is_op = True
            elif name == self.config.dim_name.head_name and self.basic_data.get_heads() != data:
                self.basic_data.set_heads(data)
                is_op = True
            elif self.basic_data.get_layers() != data:
                self.basic_data.set_layers(data)
                is_op = True
            if is_op:
                self.__add_tabel_widget()
                self.__data_choice_changed()
        return dd

    def __data_num_func(self):
        number = len(self.model_output)
        dialog = AnvnDODialog(f'Select data', number=number, data=self.basic_data.get_data_num())
        dialog.ok_handle.connect(self.__do_dialog(self.config.dim_name.data_name))
        dialog.show()

    def __layers_func(self):
        number = self.model_output.get_layer_len(self.basic_data.get_model_tokenizer_names(), self.basic_data.get_key())
        dialog = AnvnDODialog(f'Select layer', number=number, data=self.basic_data.get_layers())
        dialog.ok_handle.connect(self.__do_dialog(self.config.dim_name.layer_name))
        dialog.show()

    def __heads_func(self):
        number = self.model_output.get_head_len(self.basic_data.get_model_tokenizer_names(), self.basic_data.get_key())
        dialog = AnvnDODialog(f'Select head', number=number, data=self.basic_data.get_heads())
        dialog.ok_handle.connect(self.__do_dialog(self.config.dim_name.head_name))
        dialog.show()

    def __init_data_choice(self):
        spacing = 5
        data_choice_layout = QHBoxLayout()
        data_num = AnvnOpButton('#7dc5eb', '0', 'table', data_choice_layout,
                                alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__data_num_func)

        data_num.setToolTip('Select data')
        if len(self.model_output) <= 1:
            data_num.setDisabled(True)

        keys_combo_box = AnvnComboBox(layout=data_choice_layout, spacing=spacing)
        keys_combo_box.addItems(self.config.model_output.output_names)

        layer_but = AnvnOpButton(
            '#7dc5eb', '', 'layer', data_choice_layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__layers_func)
        layer_but.setToolTip('Select layer')
        
        head_but = AnvnOpButton(
            '#7dc5eb', '', 'head', data_choice_layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__heads_func)
        head_but.setToolTip('Select head')

        decimal_digit = AnvnComboBox(layout=data_choice_layout, spacing=spacing)
        decimal_digit.setToolTip('Select decimal digit')
        decimal_digit.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        decimal_digit.setCurrentText(str(self.basic_data.get_decimal_digit()))
        decimal_digit.currentTextChanged.connect(self.__decimal_digit_func)

        revoke_but = AnvnOpButton('#7dc5eb', '', 'revoke', data_choice_layout,
                                  alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__revoke_func)
        revoke_but.setToolTip('Revoke')
        revoke_but.setDisabled(True)

        forward_but = AnvnOpButton('#7dc5eb', '', 'forward', data_choice_layout,
                                   alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__forward_func)
        forward_but.setDisabled(True)
        forward_but.setToolTip('Forward')

        self.main_layout.addLayout(data_choice_layout)
        data_choice_layout.addStretch(0)
        return data_num, keys_combo_box,  layer_but, head_but, decimal_digit, revoke_but, forward_but

    def __decimal_digit_func(self, text):
        digit = int(text)
        self.basic_data.set_decimal_digit(digit)
        table = self.table_main.currentWidget()
        table.set_digit(digit)

    def __revoke_forward_disable(self):
        table = self.table_main.currentWidget()
        current_index = self.table_main.currentIndex()
        if table.is_start() and current_index == 0:
            self.revoke_but.setDisabled(True)
        else:
            self.revoke_but.setDisabled(False)
        if table.is_end() and current_index == self.table_main.count() - 1:
            self.forward_but.setDisabled(True)
        else:
            self.forward_but.setDisabled(False)

    def __revoke_func(self):
        table = self.table_main.currentWidget()
        if not table.revoke():
            self.table_main.setCurrentIndex(self.table_main.currentIndex() - 1)
            self.__update_current_data()
        self.__revoke_forward_disable()

    def __update_current_data(self):
        table = self.table_main.currentWidget()
        self.basic_data = table.get_basic_data().copy()
        self.__data_choice_changed()

    def __forward_func(self):
        table = self.table_main.currentWidget()
        if not table.forward():
            self.table_main.setCurrentIndex(self.table_main.currentIndex() + 1)
            self.__update_current_data()
        self.__revoke_forward_disable()

    def __data_choice_changed(self):
        self.data_num_but.setText(AnvnUtils.l2s_mto(',', self.basic_data.get_data_num(), 10))
        self.key_but.setCurrentText(self.basic_data.get_key())
        self.digit_but.setCurrentText(str(self.basic_data.get_decimal_digit()))

        if self.basic_data.get_key() == self.config.model_output.attentions or self.basic_data.get_key() == self.config.model_output.hidden_states:
            self.layer_but.show()
        else:
            self.layer_but.hide()

        if self.basic_data.get_key() == self.config.model_output.attentions:
            self.head_but.show()
        else:
            self.head_but.hide()

    def __key_changed_func(self, text):
        if self.basic_data.get_key() != text:
            self.basic_data.set_key(text)
            self.__data_choice_changed()
            self.__add_tabel_widget()

class AnvnDataOperationWidget(AnvnDockWidget):

    handle = pyqtSignal()

    def __init__(self, title='Data Operation'):
        super(AnvnDataOperationWidget, self).__init__(title)
        self.setStatusTip(title)
        self.lmo_widget = AnvnLMOWidget()
        self.lmo_widget.clicked(lambda: self.handle.emit())
    
    def set_lmo_widget(self):
        self.setWidget(self.lmo_widget)
        return self.lmo_widget

    def widget_reset(self):
        self.lmo_widget.set_data_load_value(0)
        self.lmo_widget.set_data_load_text()
        self.lmo_widget.set_model_run_text()
        self.lmo_widget.set_model_run_value(0)
        self.setWidget(self.lmo_widget)
        self.lmo_widget.set_error_message()
        self.lmo_widget.show_disabled(True)

    def injection_data(self, model_output):
        mmo = AnvnMMOWidget(model_output)
        self.setWidget(mmo)
        return mmo
