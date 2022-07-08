from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QLabel, QTableWidgetItem, QLineEdit, QTextEdit
from widget_utils import AnvnDockWidget, AnvnOpButton, AnvnComboBox, AnvnProgressBar, AnvnDialog, AnvnInformationWidget, AnvnFrame
from PyQt5.QtCore import Qt
from anvn_utils import AnvnUtils

class AnvnDODialog(AnvnDialog):
    def __init__(self, title, help, input, ok_callback, result_message, h=470, number = 500, parent=None) -> None:
        super().__init__(title, h=h, parent=parent)
        self.main_layout = QVBoxLayout(self)
        self.__set_style()
        self.setLayout(self.main_layout)
        if help is not None:
            self.__add_help(help)
            self.main_layout.addStretch(0)
        if input is not None:
            self.__add_input(input)
            self.main_layout.addStretch(0)
        if ok_callback is not None:
            self.__add_op_button(ok_callback)
        self.result_message = result_message
        self.data = []
        self.number = number

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
            else:
                result_text = self.result_message[data_analysis_result - 1]
                text_edit.setStyleSheet('''
                    color: #d81e06;
                    border-radius: 3px;
                ''')
            text_edit.setText(result_text)
        return tcf

    def __add_input(self, input):
        information = AnvnInformationWidget(input)
        lint_edit = QLineEdit()
        lint_edit.setObjectName('line_edit')
        information.add_widget(lint_edit)
        information.add_information('Result:', '#17abe3')
        result = QTextEdit()
        result.setMaximumHeight(70)
        result.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        result.setReadOnly(True)
        result.setObjectName('result')
        lint_edit.textChanged.connect(self.__text_changed_func(lint_edit, result))

        information.add_widget(result)
        self.main_layout.addWidget(information)
        information.add_stretch(0)

    def __add_op_button(self, callback_func=None):
        frame = AnvnFrame(self)
        layout = QHBoxLayout()
        layout.addStretch(0)
        AnvnOpButton('#1296db', 'OK', 'ok', layout)(callback_func)
        AnvnOpButton('#eeb174', 'Cancel', 'cancel', layout)(lambda : {
            self.close()
        })
        frame.setLayout(layout)
        self.main_layout.addWidget(frame)

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
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def get_selected(self):
        rows = self.model_.selectedRows()
        columns = self.model_.selectedColumns()
        return [r.row() for r in rows], [c.column() for c in columns]
    
    def set_items(self, data):
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.setItem(i, j, QTableWidgetItem(str(data[i][j])))


class AnvnAttentionTableWidget(AnvnTableWidget):
    def __init__(self):
        super(AnvnAttentionTableWidget, self).__init__()

    def add_data2table(self, data, ot):
        self.clear()
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]))
        self.setHorizontalHeaderLabels(ot)
        self.setVerticalHeaderLabels(ot)
        self.set_items(data)

class AnvnAttentionTableManagement(QWidget):
    def __init__(self, data, ots, iis, data_num, layers, heads):
        super(AnvnAttentionTableManagement, self).__init__()
        self.main_layout = QVBoxLayout()
        self.data_num = data_num
        self.layers = layers
        self.heads = heads
        self.data = data
        self.ots = ots
        self.iis = iis
        self.current_index = 0
        self.current_data = [(data, ots, iis, 0, 0, 0)]

        self.attention_table_widget = AnvnAttentionTableWidget()
        self.main_layout.addWidget(self.attention_table_widget)

        self.add_data2table()
        self.setLayout(self.main_layout)

    def add_data2table(self):
        data, ots, _, di, li, hi = self.current_data[self.current_index]
        self.attention_table_widget.add_data2table(data[di][li][hi], ots[di])

class AnvnStateTableWidget(AnvnTableWidget):
    def __init__(self):
        super(AnvnStateTableWidget, self).__init__()

    def add_data2table(self, data, ot):
        self.clear()
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]))
        self.setHorizontalHeaderLabels([str(i) for i in range(1, len(data[0]) + 1)])
        self.setVerticalHeaderLabels(ot)
        self.set_items(data)

class AnvnStateTableManagement(QWidget):
    def __init__(self, data, ots, iis, data_num, layers=None):
        super(AnvnStateTableManagement, self).__init__()
        self.main_layout = QVBoxLayout()
        self.data_num = data_num
        self.layers = layers
        self.data = data
        self.ots = ots
        self.iis = iis
        self.current_index = 0
        if self.layers is None:
            self.current_data = [(data, ots, iis, 0)]
        else:
            self.current_data = [(data, ots, iis, 0, 0)]
        self.state_table_widget = AnvnStateTableWidget()
        self.main_layout.addWidget(self.state_table_widget)
        self.add_data2table()
        self.setLayout(self.main_layout)
    
    def add_data2table(self):
        if self.layers is None:
            data, ots, _, di = self.current_data[self.current_index]
            self.state_table_widget.add_data2table(data[di], ots[di])
        else:
            data, ots, _, di, li = self.current_data[self.current_index]
            self.state_table_widget.add_data2table(data[di][li], ots[di])

class AnvnPoolerTableWidget(AnvnTableWidget):
    def __init__(self):
        super(AnvnPoolerTableWidget, self).__init__()

    def add_data2table(self, data, data_num):
        self.clear()
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]))
        self.setHorizontalHeaderLabels([str(i) for i in range(1, len(data[0]) + 1)])
        self.setVerticalHeaderLabels([str(i) for i in data_num])
        self.set_items(data)

class AnvnPoolerTableManagement(QWidget):
    def __init__(self, data, data_num):
        super(AnvnPoolerTableManagement, self).__init__()
        self.main_layout = QVBoxLayout()
        self.data_num = data_num
        self.data = data
        self.current_index = 0
        self.current_data = [(data, data_num)]
        self.pooler_table_widget = AnvnPoolerTableWidget()
        self.main_layout.addWidget(self.pooler_table_widget)
        self.add_data2table()
        self.setLayout(self.main_layout)

    def add_data2table(self):
        data, data_num = self.current_data[self.current_index]
        self.pooler_table_widget.add_data2table(data, data_num)

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
    def __init__(self, tokenizer, outputs, all_ots, all_iis, last_hidden_state='last_hidden_state', pooler_output='pooler_output', hidden_states='hidden_states', attentions='attentions'):
        super(AnvnMMOWidget, self).__init__()
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
        self.current_layers = [0]
        self.current_heads = [0]

        self.tokenizer = tokenizer

        self.main_layout = QVBoxLayout()
        self.layer_but, self.head_but = self.__init_data_choice()
        self.__data_choice_changed()

        self.data_table_widgets = []

        self.tables = []
        self.current_table = -1
        self.__add_tabel_widget()
        self.setLayout(self.main_layout)
        
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
        if len(self.tables) > 0:
            self.main_layout.removeWidget(self.tables[self.current_table])
        
        data, ots, iis = self.__get_table_data()
        if self.key == self.attentions:
            table_mangement = AnvnAttentionTableManagement(
                data, ots, iis, self.current_data_num, self.current_layers, self.current_heads)
            self.main_layout.addWidget(table_mangement)
        elif self.key == self.hidden_states:
            table_mangement = AnvnStateTableManagement(
                data, ots, iis, self.current_data_num, self.current_layers)
            self.main_layout.addWidget(table_mangement)
        elif self.key == self.last_hidden_state:
            table_mangement = AnvnStateTableManagement(
                data, ots, iis, self.current_data_num)
            self.main_layout.addWidget(table_mangement)
        else:
            table_mangement = AnvnPoolerTableManagement(
                data, self.current_data_num)
            self.main_layout.addWidget(table_mangement)
        self.tables.append(table_mangement)
        self.current_table += 1

    def __data_num_func(self):
        AnvnDODialog(f'Select data', help='Please enter the position of the data [0-n) separated by commas, or use [i-j] to select the data, n represents the number of pieces of data, i represents the starting data position, and j represents the ending data position.', input=f'Select data [0, {len(self.all_iis) - 1}]:', result_message=['Data analysis error.', f'The selected data is out of range [0, {len(self.all_iis) - 1}].', 'Data is empty.'], ok_callback=lambda : {}).show()

    def __layer_func(self):
        AnvnDODialog(f'Select layer', help='Please enter the position of the layer [0-n) separated by commas, or use [i-j] to select the layer, n represents the number of layers, i represents the starting layer position, and j represents the ending layer position.', input=f'Select layer [0, {len(self.outputs[self.key][0]) - 1}]:', result_message=['Layer analysis error.', f'The selected layer is out of range [0, {len(self.outputs[self.key][0]) - 1}].', 'Layer is empty.'], ok_callback=lambda : {}).show()

    def __head_func(self):
        AnvnDODialog(f'Select head', help='Please enter the position of the head [0-n) separated by commas, or use [i-j] to select the head, n represents the number of heads, i represents the starting head position, and j represents the ending head position.', input=f'Select head [0, {len(self.outputs[self.key][0][0]) - 1}]:', result_message=['Head analysis error.', f'The selected head is out of range [0, {len(self.outputs[self.key][0][0]) - 1}].', 'Head is empty.'], ok_callback=lambda : {}).show()

    def __init_data_choice(self):
        data_choice_layout = QHBoxLayout()
        data_num = AnvnOpButton('#eeb174', '0', 'data_num', data_choice_layout,
                     alignment=Qt.AlignmentFlag.AlignLeft)
        
        if len(self.all_ots) == 1:
            data_num.setDisabled(True)
        else:
            data_num(self.__data_num_func)
        
        keys_combo_box = AnvnComboBox(layout=data_choice_layout)
        keys_combo_box.addItems(self.output_keys)
        if self.attentions in self.output_keys:
            keys_combo_box.setCurrentText(self.attentions)

        self.key = keys_combo_box.currentText()
        keys_combo_box(self.key_changed_func)
        head_but = None
        layer_but = None
        if self.attentions in self.output_keys or self.hidden_states in self.output_keys:
            layer_but = AnvnOpButton(
                '#c8db8c', '--', 'layer', data_choice_layout, alignment=Qt.AlignmentFlag.AlignLeft)(self.__layer_func)
        if self.attentions in self.output_keys:
            head_but = AnvnOpButton(
                '#7dc5eb', '--', 'head', data_choice_layout, alignment=Qt.AlignmentFlag.AlignLeft)(self.__head_func)

        self.main_layout.addLayout(data_choice_layout)
        data_choice_layout.addStretch(0)
        return layer_but, head_but

    def __data_choice_changed(self):
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

    def key_changed_func(self, text):
        self.key = text
        self.__data_choice_changed()
        self.__add_tabel_widget()

class AnvnModelOperationWidget(AnvnDockWidget):
    def __init__(self, title='Model Operation', parent=None):
        super(AnvnModelOperationWidget, self).__init__(title, parent)
        self.outputs = None
        self.tokenizer = None
        self.all_ots = None
        self.all_iis = None
        self.setStatusTip(title)
        self.anvn_lmo_widget = AnvnLMOWidget()
        self.anvn_lmo_widget.clicked(self.injection_data_func)
        self.setWidget(self.anvn_lmo_widget)

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
        self.anvn_lmo_widget.set_model_load_text(text)

    def set_data_load_text(self, text=None):
        self.anvn_lmo_widget.set_data_load_text(text)

    def set_model_run_text(self, text=None):
        self.anvn_lmo_widget.set_model_run_text(text)

    def model_load_stop(self):
        self.anvn_lmo_widget.model_load_stop()

    def set_data_load_value(self, value):
        self.anvn_lmo_widget.set_data_load_value(value)

    def set_model_run_value(self, value):
        self.anvn_lmo_widget.set_model_run_value(value)

    def widget_reset(self):
        self.outputs = None
        self.tokenizer = None
        self.all_iis = None
        self.all_ots = None
        self.set_data_load_value(0)
        self.set_data_load_text()
        self.set_model_run_text()
        self.set_model_run_value(0)
        self.setWidget(self.anvn_lmo_widget)
        self.anvn_lmo_widget.disabled(True)

    def disabled(self, disabled):
        self.anvn_lmo_widget.disabled(disabled)

    def injection_data_func(self):
        self.setWidget(AnvnMMOWidget(
            self.tokenizer, self.outputs, self.all_ots, self.all_iis))
