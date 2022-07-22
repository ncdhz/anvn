from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QStackedWidget
from anvn_widget_utils import AnvnDockWidget, AnvnOpButton, AnvnComboBox, AnvnProgressBar, AnvnDialog, AnvnInformationWidget, AnvnFrame
from PyQt5.QtCore import Qt
from anvn_utils import AnvnUtils
from anvn_table_management import AnvnAttentionsTableManagement, AnvnHiddenStatesTableManagement, AnvnLastHiddenStateTableManagement, AnvnPoolerTableManagement

class AnvnDODialog(AnvnDialog):
    def __init__(self, title, help, input, ok_callback, result_message, number, data, h=470, parent=None) -> None:
        super().__init__(title, h=h, parent=parent)
        self.data = data
        self.result_message = result_message
        self.number = number
        self.ok_callback = ok_callback

        self.main_layout = QVBoxLayout(self)
        self.__set_style()
        self.setLayout(self.main_layout)
        self.__add_help(help)
        self.main_layout.addStretch(0)
        lint_edit, result_view = self.__add_input(input)
        self.main_layout.addStretch(0)
        self.ok = self.__add_op_button()

        lint_edit.textChanged.connect(
            self.__text_changed_func(lint_edit, result_view))
        lint_edit.setText(AnvnUtils.list2str(',', self.data))
        self.ok.setDisabled(True)

    def get_data(self):
        return self.data

    def __add_help(self, help):
        information = AnvnInformationWidget('Help:')
        self.main_layout.addWidget(information)
        information.add_information(help, '#eeb174')
        information.add_stretch(0)

    def __data_analysis(self, str_data):
        '''
        return: 0: success, 1: error, 2: array out of bounds, 3: no data
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
                        if i >= self.number:
                            return 2
                        data.add(i)
                else:
                    if int(sd) >= self.number:
                        return 2
                    data.add(int(sd))
            pass
        except Exception:
            return 1
        if len(data) == 0:
            return 3

        data = list(data)
        data.sort()
        self.data = data
        return 0

    def __text_changed_func(self, lint_edit, text_edit):
        def tcf():
            data_analysis_result = self.__data_analysis(lint_edit.text())
            result_text = ''
            if data_analysis_result == 0:
                result_text = ','.join(str(i) for i in self.data)
                text_edit.setStyleSheet('''
                    color: #8a8a8a;
                    border-radius: 3px;
                ''')
                self.ok.setDisabled(False)
            else:
                result_text = self.result_message[data_analysis_result - 1]
                text_edit.setStyleSheet('''
                    color: #d81e06;
                    border-radius: 3px;
                ''')
                self.ok.setDisabled(True)
            text_edit.setText(result_text)
        return tcf

    def __add_input(self, input):
        information = AnvnInformationWidget(input)
        lint_edit = QLineEdit()
        lint_edit.setObjectName('line_edit')
        information.add_widget(lint_edit)
        information.add_information('Result:', '#17abe3')
        lint_edit.setPlaceholderText('e.g. 1,2,7-10,12')
        result_view = QTextEdit()
        result_view.setMaximumHeight(70)
        result_view.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        result_view.setReadOnly(True)
        result_view.setObjectName('result')

        information.add_widget(result_view)
        self.main_layout.addWidget(information)
        information.add_stretch(0)
        return lint_edit, result_view

    def __ok_func(self):
        self.ok_callback(self.data)
        self.close()

    def __add_op_button(self):
        frame = AnvnFrame(self)
        layout = QHBoxLayout()
        layout.addStretch(0)
        ok = AnvnOpButton('#1296db', 'OK', 'ok', layout)(self.__ok_func)
        AnvnOpButton('#eeb174', 'Cancel', 'cancel', layout)(lambda: {
            self.close()
        })
        ok.setDisabled(True)
        frame.setLayout(layout)
        self.main_layout.addWidget(frame)
        return ok

    def __set_style(self):
        self.setStyleSheet('''
            #line_edit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 3px;
                color: #8a8a8a;
            }
            #result {
                color: #8a8a8a;
                border-radius: 3px;
            }
        ''')

class AnvnLMOWidget(QWidget):
    def __init__(self) -> None:
        super(AnvnLMOWidget, self).__init__()
        self.main_layout = QVBoxLayout()
        self.model_load_label, self.model_load_progress_bar = self.__model_load()
        self.data_load_label, self.data_load_progress_bar = self.__data_load()
        self.model_run_label, self.model_run_progress_bar = self.__model_run()
        self.show_button = self.__load_button()
        self.main_layout.addStretch(0)
        self.setLayout(self.main_layout)

    def __load_progress_bar(self, color, text, maximum):
        widget = QWidget()
        widget.setStyleSheet('''
            QWidget {
                margin: 0px 8px;
            }
            QWidget QLabel {
                color: ''' + color + ''';
                padding-bottom: 5px;
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

    def disabled(self, disabled):
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
    def __init__(self, tokenizer, outputs, all_ots, all_iis, last_hidden_state='last_hidden_state', pooler_output='pooler_output', hidden_states='hidden_states', attentions='attentions', callback_func=None):
        super(AnvnMMOWidget, self).__init__()
        self.callback_func = callback_func
        self.outputs = outputs
        self.output_keys = list(outputs.keys())
        self.all_ots = all_ots
        self.all_iis = all_iis

        self.key = None
        self.last_hidden_state = last_hidden_state
        self.pooler_output = pooler_output
        self.hidden_states = hidden_states
        self.attentions = attentions

        self.current_data_num = [0]
        self.current_layers = None
        self.current_heads = None

        self.tokenizer = tokenizer
        self.digit = 5

        self.main_layout = QVBoxLayout()

        self.data_num_but, self.key_but, self.layer_but, self.head_but, self.digit_but, self.revoke_but, self.forward_but = self.__init_data_choice()

        self.setLayout(self.main_layout)

        self.table_main = QStackedWidget()
        self.main_layout.addSpacing(15)
        self.main_layout.addWidget(self.table_main)
        self.current_table = -1

        self.__init_data_show()

        self.main_layout.addStretch(0)
        # add key connect, init table
        self.key_but(self.__key_changed_func)
        if self.attentions in self.output_keys:
            self.key_but.setCurrentText(self.attentions)

    def __show_func(self):
        if self.callback_func is not None:
            table = self.table_main.currentWidget()
            self.callback_func(table)

    def __init_data_show(self):
        data_show = QHBoxLayout()
        data_show.addStretch(0)
        AnvnOpButton('#1296db', 'Show', 'show', data_show)(self.__show_func)
        self.main_layout.addLayout(data_show)

    def __get_table_data(self):
        data, ots, iis = [], [], []
        output = self.outputs[self.key]
        for i in self.current_data_num:
            ots.append(self.all_ots[i])
            iis.append(self.all_iis[i])
            if self.key == self.last_hidden_state or self.key == self.pooler_output:
                data.append(output[i])
            else:
                dataj = []
                for j in self.current_layers:
                    if self.key == self.hidden_states:
                        dataj.append(output[i][j])
                    else:
                        datak = []
                        for k in self.current_heads:
                            datak.append(output[i][j][k])
                        dataj.append(datak)
                data.append(dataj)
        return data, ots, iis

    def __add_tabel_widget(self):
        self.__remove_current_after_table()

        if self.current_table >= 0:
            tabel = self.table_main.currentWidget()
            tabel.delete_index_after()

        data, ots, iis = self.__get_table_data()
        if self.key == self.attentions:
            table_mangement = AnvnAttentionsTableManagement(
                data, ots, iis, self.current_data_num, self.current_layers, self.current_heads, key=self.key, digit=self.digit, tokenizer=self.tokenizer)
        elif self.key == self.hidden_states:
            table_mangement = AnvnHiddenStatesTableManagement(
                data, ots, iis, self.current_data_num, self.current_layers, key=self.key, digit=self.digit, tokenizer=self.tokenizer)
        elif self.key == self.last_hidden_state:
            table_mangement = AnvnLastHiddenStateTableManagement(
                data, ots, iis, self.current_data_num, key=self.key, digit=self.digit, tokenizer=self.tokenizer)
        else:
            table_mangement = AnvnPoolerTableManagement(
                data, self.current_data_num, key=self.key, digit=self.digit)
        table_mangement.change_event(self.__table_changed_func)
        self.table_main.addWidget(table_mangement)
        self.current_table += 1
        self.table_main.setCurrentIndex(self.current_table)
        self.__revoke_forward_disable()

    def __remove_current_after_table(self):
        for i in range(self.table_main.count() - 1, self.current_table, -1):
            self.table_main.removeWidget(self.table_main.widget(i))

    def __table_changed_func(self):
        self.__remove_current_after_table()
        self.__revoke_forward_disable()

    def __set_data_num(self, data):
        self.current_data_num = data
        self.__add_tabel_widget()
        self.__data_choice_changed()

    def __set_layers(self, layers):
        self.current_layers = layers
        self.__add_tabel_widget()
        self.__data_choice_changed()

    def __set_heads(self, heads):
        self.current_heads = heads
        self.__add_tabel_widget()
        self.__data_choice_changed()

    def __data_num_func(self):
        AnvnDODialog(f'Select data', help='Please enter the position of the data [0-n) separated by commas, or use [i-j] to select the data, n represents the number of pieces of data, i represents the starting data position, and j represents the ending data position.',
                     input=f'Select data [0, {len(self.all_iis) - 1}]:', result_message=['Data analysis error.', f'The selected data is out of range [0, {len(self.all_iis) - 1}].', 'Data is empty.'], ok_callback=self.__set_data_num, number=len(self.all_iis), data=self.current_data_num).show()

    def __layers_func(self):
        AnvnDODialog(f'Select layer', help='Please enter the position of the layer [0-n) separated by commas, or use [i-j] to select the layer, n represents the number of layers, i represents the starting layer position, and j represents the ending layer position.', input=f'Select layer [0, {len(self.outputs[self.key][0]) - 1}]:', result_message=[
                     'Layer analysis error.', f'The selected layer is out of range [0, {len(self.outputs[self.key][0]) - 1}].', 'Layer is empty.'], ok_callback=self.__set_layers, number=len(self.outputs[self.key][0]), data=self.current_layers).show()

    def __heads_func(self):
        AnvnDODialog(f'Select head', help='Please enter the position of the head [0-n) separated by commas, or use [i-j] to select the head, n represents the number of heads, i represents the starting head position, and j represents the ending head position.', input=f'Select head [0, {len(self.outputs[self.key][0][0]) - 1}]:', result_message=[
                     'Head analysis error.', f'The selected head is out of range [0, {len(self.outputs[self.key][0][0]) - 1}].', 'Head is empty.'], ok_callback=self.__set_heads, number=len(self.outputs[self.key][0][0]), data=self.current_heads).show()

    def __init_data_choice(self):
        spacing = 5
        data_choice_layout = QHBoxLayout()
        data_num = AnvnOpButton('#eeb174', '0', 'data_num', data_choice_layout,
                                alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)
        data_num.setToolTip('Select data')
        if len(self.all_ots) == 1:
            data_num.setDisabled(True)
        else:
            data_num(self.__data_num_func)

        keys_combo_box = AnvnComboBox(layout=data_choice_layout, spacing=spacing)
        keys_combo_box.addItems(self.output_keys)

        head_but = None
        layer_but = None
        if self.attentions in self.output_keys or self.hidden_states in self.output_keys:
            layer_but = AnvnOpButton(
                '#c8db8c', '--', 'layer', data_choice_layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__layers_func)
            layer_but.setToolTip('Select layer')
        if self.attentions in self.output_keys:
            head_but = AnvnOpButton(
                '#7dc5eb', '--', 'head', data_choice_layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__heads_func)
            head_but.setToolTip('Select head')

        decimal_digit = AnvnComboBox(layout=data_choice_layout, spacing=spacing)
        decimal_digit.setToolTip('Select decimal digit')
        decimal_digit.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        decimal_digit.setCurrentText(str(self.digit))
        decimal_digit.currentTextChanged.connect(self.__decimal_digit_func)

        revoke_but = AnvnOpButton('#7dc5eb', 'Revoke', 'revoke', data_choice_layout,
                                  alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__revoke_func)
        revoke_but.setDisabled(True)
        forward_but = AnvnOpButton('#7dc5eb', 'Forward', 'forward', data_choice_layout,
                                   alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__forward_func)
        forward_but.setDisabled(True)

        self.main_layout.addLayout(data_choice_layout)
        data_choice_layout.addStretch(0)
        return data_num, keys_combo_box,  layer_but, head_but, decimal_digit, revoke_but, forward_but

    def __decimal_digit_func(self, text):
        if self.digit != int(text):
            self.digit = int(text)
            table = self.table_main.currentWidget()
            table.set_digit(self.digit)

    def __revoke_forward_disable(self):
        table = self.table_main.currentWidget()
        if table.is_start() and self.current_table == 0:
            self.revoke_but.setDisabled(True)
        else:
            self.revoke_but.setDisabled(False)
        if table.is_end() and self.current_table == self.table_main.count() - 1:
            self.forward_but.setDisabled(True)
        else:
            self.forward_but.setDisabled(False)

    def __revoke_func(self):
        table = self.table_main.currentWidget()
        if not table.revoke():
            self.current_table -= 1
            self.table_main.setCurrentIndex(self.current_table)
            self.__update_current_data()
        self.__revoke_forward_disable()

    def __update_current_data(self):
        table = self.table_main.currentWidget()
        self.current_data_num = table.get_data_num()
        self.current_layers = table.get_layers()
        self.current_heads = table.get_heads()
        self.key = table.get_key()
        self.digit = table.get_digit()
        self.__data_choice_changed()

    def __forward_func(self):
        table = self.table_main.currentWidget()
        if not table.forward():
            self.current_table += 1
            self.table_main.setCurrentIndex(self.current_table)
            self.__update_current_data()
        self.__revoke_forward_disable()

    def __data_choice_changed(self):
        self.data_num_but.setText(AnvnUtils.l2s_mto(
            ',', self.current_data_num, 10))
        self.key_but.setCurrentText(self.key)
        self.digit_but.setCurrentText(str(self.digit))
        if self.key == self.attentions or self.key == self.hidden_states:
            self.layer_but.setText(AnvnUtils.l2s_mto(
                ',', self.current_layers, 10))
            self.layer_but.setDisabled(False)
        if self.key == self.attentions:
            self.head_but.setText(AnvnUtils.l2s_mto(
                ',', self.current_heads, 10))
            self.head_but.setDisabled(False)

        if self.key == self.hidden_states:
            self.head_but.setText('--')
            self.head_but.setDisabled(True)

        if self.key == self.last_hidden_state or self.key == self.pooler_output:
            self.layer_but.setText('--')
            self.layer_but.setDisabled(True)
            self.head_but.setText('--')
            self.head_but.setDisabled(True)

    def __layers_heads_init(self):
        self.current_heads = [0]
        self.current_layers = [0]

    def __key_changed_func(self, text):
        if self.key != text:
            self.key = text
            self.__layers_heads_init()
            self.__data_choice_changed()
            self.__add_tabel_widget()


class AnvnDataOperationWidget(AnvnDockWidget):
    def __init__(self, title='Model Operation', parent=None, callback_func=None):
        super(AnvnDataOperationWidget, self).__init__(title, parent)
        self.outputs = None
        self.tokenizer = None
        self.all_ots = None
        self.all_iis = None
        self.setStatusTip(title)
        self.lmo_widget = AnvnLMOWidget()
        self.lmo_widget.clicked(self.injection_data_func)
        self.setWidget(self.lmo_widget)
        self.callback_func = callback_func

    def set_callback_func(self, callback):
        self.callback_func = callback

    def set_outputs(self, outputs):
        self.outputs = outputs
        return self

    def set_tokenizer(self, tokenizer):
        self.tokenizer = tokenizer
        return self

    def set_all_ots(self, all_ots):
        self.all_ots = all_ots
        return self

    def sel_all_iis(self, all_iis):
        self.all_iis = all_iis
        return self

    def set_model_load_text(self, text=None):
        self.lmo_widget.set_model_load_text(text)

    def set_data_load_text(self, text=None):
        self.lmo_widget.set_data_load_text(text)

    def set_model_run_text(self, text=None):
        self.lmo_widget.set_model_run_text(text)

    def model_load_stop(self):
        self.lmo_widget.model_load_stop()

    def set_data_load_value(self, value):
        self.lmo_widget.set_data_load_value(value)

    def set_model_run_value(self, value):
        self.lmo_widget.set_model_run_value(value)

    def widget_reset(self):
        self.outputs = None
        self.tokenizer = None
        self.all_iis = None
        self.all_ots = None
        self.set_data_load_value(0)
        self.set_data_load_text()
        self.set_model_run_text()
        self.set_model_run_value(0)
        self.setWidget(self.lmo_widget)
        self.lmo_widget.disabled(True)

    def disabled(self, disabled):
        self.lmo_widget.disabled(disabled)

    def __mmo_callback_func(self, table):
        if self.callback_func is not None:
            self.callback_func(table)

    def injection_data_func(self):
        self.setWidget(AnvnMMOWidget(
            self.tokenizer, self.outputs, self.all_ots, self.all_iis, callback_func=self.__mmo_callback_func))
