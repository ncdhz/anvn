from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QStackedWidget
from anvn_widget_utils import AnvnOpButton, AnvnTableWidget, AnvnComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from anvn_utils import AnvnUtils
from anvn_data import AnvnTableData
from anvn_config import AnvnConfig
import numpy as np
from anvn_data import AnvnBasicData, AnvnModelOutputData

class AnvnTableManagement(QFrame):
    handle = pyqtSignal()

    def __init__(self, data: AnvnTableData):
        super().__init__()
        self.data = data
        self.main_layout = QVBoxLayout()
        self.setObjectName('table_management')
        self.setLayout(self.main_layout)
        self.config = data.get_config()
        self.remove_but, self.fuse_cb, self.fuse_rows_but, self.fuse_columns_but, self.data_layer_head_cb, self.up_but, self.data_layer_head_text, self.down_but = self.__init_table_op()
        self.tables_widget = QStackedWidget()
        self.main_layout.addWidget(self.tables_widget)
        self.data2table()
        self.__set_style()

    def __op_func(self, callback):
        def op():
            table = self.tables_widget.currentWidget()
            rows, columns = table.get_selected()
            if callback == self.remove:
                self.data.ops.insert(self.data.op_index + 1, ((self.remove, rows, columns), self.data.ops[self.data.op_index][1]))
            elif callback == self.fuse_rows:
                self.data.ops.insert(self.data.op_index + 1, ((self.fuse_rows, rows, self.fuse_cb.currentText()), self.data.ops[self.data.op_index][1]))
            elif callback == self.fuse_columns:
                self.data.ops.insert(self.data.op_index + 1, ((self.fuse_columns, columns, self.fuse_cb.currentText()), self.data.ops[self.data.op_index][1]))
            elif callback == self.down:
                self.down(self.data_layer_head_cb.currentText())
            elif callback == self.up:
                self.up(self.data_layer_head_cb.currentText())

            self.data.set_op_index(self.data.get_op_index() + 1)
            self.data2table()
        return op

    def fuse_rows(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, rows, index, fuse_key):
        pass

    def fuse_columns(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, columns, fuse_key):
        pass

    def remove(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, rows, columns):
        pass

    def down(self, key):
        op1 = self.data.ops[self.data.op_index][1].copy()
        if key == self.config.dim_name.data_name:
            op1[1] -= 1
        elif key == self.config.dim_name.layer_name:
            op1[2] -= 1
        else:
            op1[3] -= 1
        op1[-1] = key
        self.data.ops.insert(self.data.op_index + 1, (None, op1))

    def up(self, key):
        op1 = self.data.ops[self.data.op_index][1].copy()
        if key == self.config.dim_name.data_name:
            op1[1] += 1
        elif key == self.config.dim_name.layer_name:
            op1[2] += 1
        else:
            op1[3] += 1
        op1[-1] = key

        self.data.ops.insert(self.data.op_index + 1, (None, op1))

    def __init_table_op(self):
        spacing = 5
        table_op = QFrame()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        remove_but = AnvnOpButton('#d81e06', '', 'remove', layout,
                                  alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__op_func(self.remove))
        remove_but.setToolTip('Remove selected rows and columns.')
        remove_but.setDisabled(True)

        fuse_cb = AnvnComboBox(layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)
        fuse_cb.addItems(list(AnvnUtils.get_fuse_op().keys()))
        fuse_cb.setCurrentText(self.data.get_fuse_key())
        fuse_cb.setDisabled(True)

        fuse_rows_but = AnvnOpButton('#17abe3', '', 'fuse_rows', layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__op_func(self.fuse_rows))
        fuse_rows_but.setToolTip('Fuse selected rows.')
        fuse_rows_but.setDisabled(True)

        fuse_columns_but = AnvnOpButton('#17abe3', '', 'fuse_columns', layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__op_func(self.fuse_columns))
        fuse_columns_but.setDisabled(True)
        fuse_columns_but.setToolTip('Fuse selected columns.')

        data_layer_head_cb = None
        up_but = None
        down_but = None
        data_layer_head_text = None
        
        if self.__class__ is not AnvnPoolerTableManagement:
            
            items = []
            if self.data.get_data_len() > 1:
                items.append(self.config.dim_name.data_name)
            if self.__class__ is not AnvnLastHiddenStateTableManagement and self.data.get_layer_len(self.data.get_model_tokenizer_key()) > 1:
                items.append(self.config.dim_name.layer_name)
            if self.__class__ is AnvnAttentionsTableManagement and self.data.get_head_len(self.data.get_model_tokenizer_key()) > 1:
                items.append(self.config.dim_name.head_name)

            if len(items) != 0:
                self.data.set_dim_name(items[0])

                data_layer_head_cb = AnvnComboBox(layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)
                data_layer_head_cb.addItems(items)
                data_layer_head_cb.currentTextChanged.connect(self.__refresh_disable)
                if len(items) == 1:
                    data_layer_head_cb.hide()

                down_but = AnvnOpButton('#17abe3', '', 'down', layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__op_func(self.down))

                data_layer_head_text = QLabel()
                data_layer_head_text.setObjectName('data_layer_head_text')
                layout.addWidget(data_layer_head_text)

                up_but = AnvnOpButton('#17abe3', '', 'up', layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__op_func(self.up))
            
        layout.addStretch(0)
        table_op.setLayout(layout)
        self.main_layout.addWidget(table_op)
        return remove_but, fuse_cb, fuse_rows_but, fuse_columns_but, data_layer_head_cb, up_but, data_layer_head_text, down_but

    @staticmethod
    def get_table_management(data, key, config: AnvnConfig):
        if key == config.model_output.attentions:
            table_mangement = AnvnAttentionsTableManagement(data)
        elif key == config.model_output.hidden_states:
            table_mangement = AnvnHiddenStatesTableManagement(data)
        elif key == config.model_output.last_hidden_state:
            table_mangement = AnvnLastHiddenStateTableManagement(data)
        else:
            table_mangement = AnvnPoolerTableManagement(data)
        return table_mangement

    @staticmethod
    def get_table_data(basic_data: AnvnBasicData, model_output: AnvnModelOutputData, config: AnvnConfig):
        
        data, all_ots, all_iis = model_output.get_data(basic_data.get_model_tokenizer_names(), basic_data.get_key(), basic_data.get_data_num(), basic_data.get_heads(), basic_data.get_layers())

        vertical_ids = None
        horizontal_ids = None

        if basic_data.get_key() == config.model_output.attentions:
            horizontal_headers = all_ots
            vertical_headers = all_ots
            horizontal_ids = all_iis
            vertical_ids = all_iis
        
        elif basic_data.get_key() == config.model_output.pooler_output:
            
            for key in data:
                data[key] = np.stack(data[key])

            vertical_headers = [str(i) for i in basic_data.get_data_num()]
            horizontal_headers = {}
            hidden_len = model_output.get_hidden_len(basic_data.get_model_tokenizer_names(), basic_data.get_key())
            for k in all_iis:
                horizontal_headers[k] = AnvnUtils.range_str(1, hidden_len[k] + 1)
        else:
            vertical_headers = all_ots
            vertical_ids = all_iis
            horizontal_headers = {}
            hidden_len = model_output.get_hidden_len(basic_data.get_model_tokenizer_names(), basic_data.get_key())
            for k in all_iis:
                horizontal_headers[k] = AnvnUtils.n_range_str(len(basic_data.get_data_num()), 1, hidden_len[k] + 1)

        return AnvnTableData(data, basic_data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, model_output.get_tokenizers(), config)
    
    def set_digit(self):
        pass

    def get_data(self):
        return self.data

    def __set_style(self):
        self.setStyleSheet('''
            #table_management {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
            }
            #data_layer_head_text {
                color: #17abe3;
                padding: 5px;
            }
        ''')
    
    def data2table(self):
        self.__refresh_disable()

        data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids = self.data.copy_op_message()

        for i in range(len(self.data.ops)):
            if self.data.ops[i][0] is not None:
                op = self.data.ops[i][0]
                data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids = op[0](data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, i, *op[1:])

        return data, horizontal_headers, vertical_headers
    
    def __refresh_disable(self, name=None):
        if name is None:
            name = self.data.get_dim_name()
        
        self.fuse_cb.setCurrentText(self.data.get_fuse_key())

        if self.down_but is not None and self.up_but is not None and self.data_layer_head_text is not None and self.data_layer_head_cb is not None:
            if self.data_layer_head_cb.currentText() != name:
                self.data_layer_head_cb.setCurrentText(name)
            if name == self.config.dim_name.data_name:
                if self.data.get_data_index() == 0:
                    self.down_but.setDisabled(True)
                else:
                    self.down_but.setDisabled(False)
                if self.data.get_data_index() >= self.data.get_data_len() - 1:
                    self.up_but.setDisabled(True)
                else:
                    self.up_but.setDisabled(False)
                self.data_layer_head_text.setText(name + ':' + str(self.data.get_data_num()[self.data.get_data_index()]))

            elif name == self.config.dim_name.layer_name:
                if self.data.get_layer_index() == 0:
                    self.down_but.setDisabled(True)
                else:
                    self.down_but.setDisabled(False)
                if self.data.get_layer_index() >= self.data.get_layer_len(self.data.get_model_tokenizer_key()) - 1:
                    self.up_but.setDisabled(True)
                else:
                    self.up_but.setDisabled(False)
                self.data_layer_head_text.setText(name + ':' + str(self.data.get_layers()[self.data.get_model_tokenizer_key()][self.data.get_layer_index()]))
        
            elif name == self.config.dim_name.head_name:
                if self.data.get_head_index() == 0:
                    self.down_but.setDisabled(True)
                else:
                    self.down_but.setDisabled(False)
                if self.data.get_head_index() >= self.data.get_head_len(self.data.get_model_tokenizer_key()) - 1:
                    self.up_but.setDisabled(True)
                else:
                    self.up_but.setDisabled(False)
                self.data_layer_head_text.setText(name + ':' + str(self.data.get_heads()[self.data.get_model_tokenizer_key()][self.data.get_head_index()]))
            
    def add_table(self, table):
        self.remove_current_after_table()
        self.tables_widget.addWidget(table)
        self.tables_widget.setCurrentWidget(table)

    def is_start(self):
        return self.tables_widget.currentIndex() == 0

    def is_end(self):
        return self.tables_widget.currentIndex() == self.tables_widget.count() - 1
    
    def revoke(self):
        if self.is_start():
            return False
        index = self.tables_widget.currentIndex()
        self.tables_widget.setCurrentIndex(index - 1)
        self.data.set_op_index(index - 1)
        self.__refresh_disable()
        return True
    
    def forward(self):
        if self.is_end():
            return False
        index = self.tables_widget.currentIndex()
        self.tables_widget.setCurrentIndex(index + 1)
        self.data.set_op_index(index + 1)
        self.__refresh_disable()
        return True

    def remove_current_after_table(self):
        for i in range(self.tables_widget.count() - 1, self.tables_widget.currentIndex(), -1):
            self.tables_widget.removeWidget(self.tables_widget.widget(i))

    def table_selection_func(self, table):
        def ts():
            rows, columns = table.get_selected()
            
            if len(rows) > 1 or len(columns) > 1:
                self.fuse_cb.setDisabled(False)
            else:
                self.fuse_cb.setDisabled(True)
            
            if len(rows) > 1:
                self.fuse_rows_but.setDisabled(False)
            else:
                self.fuse_rows_but.setDisabled(True)
            
            if len(columns) > 1:
                self.fuse_columns_but.setDisabled(False)
            else:
                self.fuse_columns_but.setDisabled(True)
            
            if (len(rows) == 0 and len(columns) == 0) or table.columnCount() == len(columns) or table.rowCount() == len(rows):
                self.remove_but.setDisabled(True)
            else:
                self.remove_but.setDisabled(False)
        return ts

class AnvnAttentionsTableManagement(AnvnTableManagement):
    def __init__(self, data: AnvnTableData):
        super(AnvnAttentionsTableManagement, self).__init__(data)
    
    def data2table(self):
        data, horizontal_headers, vertical_headers = super().data2table()
        table = AnvnTableWidget()
        table.itemSelectionChanged.connect(self.table_selection_func(table))
        table.data2table(data[self.data.get_model_tokenizer_key()][self.data.get_data_index()][self.data.get_layer_index()][self.data.get_head_index()], horizontal_headers[self.data.get_model_tokenizer_key()][self.data.get_data_index()], vertical_headers[self.data.get_model_tokenizer_key()][self.data.get_data_index()], self.data.get_decimal_digit())
        self.add_table(table)

    def remove(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, rows, columns):
        di = self.data.get_data_index(index)
        key = self.data.get_model_tokenizer_key(index)
        vertical_headers[key][di] = np.delete(vertical_headers[key][di], rows, axis=0)
        vertical_ids[key][di] = np.delete(vertical_ids[key][di], rows, axis=0)
        horizontal_headers[key][di] = np.delete(horizontal_headers[key][di], columns, axis=0)
        horizontal_ids[key][di] = np.delete(horizontal_ids[key][di], columns, axis=0)
        data[key][di] = np.delete(data[key][di], rows, axis=-2)
        data[key][di] = np.delete(data[key][di], columns, axis=-1)
        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids
    
    def fuse_rows(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, rows, index, fuse_key):

        di = self.data.get_data_index(index)
        key = self.data.get_model_tokenizer_key(index)

        rows_delete_first, rows_first = AnvnUtils.delete_first(rows)
        rows_merge = data[key][di][:,:, rows]
        rows_merge = AnvnUtils.get_fuse_op()[fuse_key](rows_merge, -2)

        data[key][di] = np.delete(data[key][di], rows_delete_first, axis=-2)
        data[key][di][:, :, rows_first] = rows_merge

        vertical_headers[key][di] = np.delete(vertical_headers[key][di], rows_delete_first, axis=0)
        ver_ids = vertical_ids[key][di][rows]
        ver_ids = AnvnUtils.flatten_list(ver_ids)
        vertical_ids[key][di] = np.delete(vertical_ids[key][di], rows_delete_first, axis=0)
        
        id = self.data.get_tokenizer(key).decode(ver_ids)
        vertical_headers[key][di][rows_first] = id
        vertical_ids[key][di][rows_first] = ver_ids

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids
    
    def fuse_columns(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, columns, fuse_key):

        di = self.data.get_data_index(index)
        key = self.data.get_model_tokenizer_key(index)

        columns_delete_first, columns_first = AnvnUtils.delete_first(columns)
        columns_merge = data[key][di][:, :, :, columns]
        columns_merge = AnvnUtils.get_fuse_op()[fuse_key](columns_merge, -1)
        data[key][di] = np.delete(data[di], columns_delete_first, axis=-1)
        data[key][di][:, :, :, columns_first] = columns_merge

        horizontal_headers[key][di] = np.delete(horizontal_headers[key][di], columns_delete_first, axis=0)
        hor_ids = horizontal_ids[key][di][columns]
        hor_ids = AnvnUtils.flatten_list(hor_ids)
        horizontal_ids[key][di] = np.delete(horizontal_ids[key][di], columns_delete_first, axis=0)

        id = self.data.get_tokenizer(key).decode(hor_ids)
        horizontal_headers[key][di][columns_first] = id
        horizontal_ids[key][di][columns_first] = hor_ids

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids

class AnvnHiddenStatesTableManagement(AnvnTableManagement):
    def __init__(self, data: AnvnTableData):
        super(AnvnHiddenStatesTableManagement, self).__init__(data)
    
    def data2table(self):
        data, horizontal_headers, vertical_headers = super().data2table()
        table = AnvnTableWidget()
        table.itemSelectionChanged.connect(self.table_selection_func(table))
        table.data2table(data[self.data.get_model_tokenizer_key()][self.data.get_data_index()][self.data.get_layer_index()], horizontal_headers[self.data.get_model_tokenizer_key()][self.data.get_data_index()], vertical_headers[self.data.get_model_tokenizer_key()][self.data.get_data_index()], self.data.get_decimal_digit())
        self.add_table(table)
    
    def remove(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, rows, columns):
        di = self.data.get_data_index(index)
        key = self.data.get_model_tokenizer_key(index)

        horizontal_headers[key][di] = np.delete(horizontal_headers[key][di], columns, axis=0)
        vertical_headers[key][di] = np.delete(vertical_headers[key][di], rows, axis=0)
        vertical_ids[key][di] = np.delete(vertical_ids[key][di], rows, axis=0)

        data[key][di] = np.delete(data[key][di], rows, axis=-2)
        data[key][di] = np.delete(data[key][di], columns, axis=-1)

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids

    def fuse_rows(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, rows, index, fuse_key):
        di = self.data.get_data_index(index)
        key = self.data.get_model_tokenizer_key(index)

        rows_delete_first, rows_first = AnvnUtils.delete_first(rows)
        rows_merge = data[key][di][:, rows]
        rows_merge = AnvnUtils.get_fuse_op()[fuse_key](rows_merge, -2)
        data[key][di] = np.delete(data[key][di], rows_delete_first, axis=-2)
        data[key][di][:, rows_first] = rows_merge

        vertical_headers[key][di] = np.delete(vertical_headers[key][di], rows_delete_first, axis=0)
        ver_ids = vertical_ids[key][di][rows]
        ver_ids = AnvnUtils.flatten_list(ver_ids)
        vertical_ids[key][di] = np.delete(vertical_ids[key][di], rows_delete_first, axis=0)

        id = self.data.get_tokenizer(key).decode(ver_ids)
        vertical_headers[key][di][rows_first] = id
        vertical_ids[key][di][rows_first] = ver_ids

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids
    
    def fuse_columns(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, columns, fuse_key):
        di = self.data.get_data_index(index)
        key = self.data.get_model_tokenizer_key(index)

        columns_delete_first, columns_first = AnvnUtils.delete_first(columns)
        columns_merge = data[key][di][:, :, columns]
        columns_merge = AnvnUtils.get_fuse_op()[fuse_key](columns_merge, -1)
        data[key][di] = np.delete(data[key][di], columns_delete_first, axis=-1)
        data[key][di][:, :, columns_first] = columns_merge

        hors = horizontal_headers[key][di][columns]
        horizontal_headers[key][di] = np.delete(horizontal_headers[key][di], columns_delete_first, axis=0)
        horizontal_headers[key][di][columns_first] = ','.join(hors)

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids

class AnvnLastHiddenStateTableManagement(AnvnTableManagement):
    def __init__(self, data: AnvnTableData):
        super(AnvnLastHiddenStateTableManagement, self).__init__(data)
    
    def data2table(self):
        data, horizontal_headers, vertical_headers = super().data2table()
        table = AnvnTableWidget()
        table.itemSelectionChanged.connect(self.table_selection_func(table))
        table.data2table(data[self.data.get_model_tokenizer_key()][self.data.get_data_index()], horizontal_headers[self.data.get_model_tokenizer_key()][self.data.get_data_index()], vertical_headers[self.data.get_model_tokenizer_key()][self.data.get_data_index()], self.data.get_decimal_digit())
        self.add_table(table)
    
    def remove(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, rows, columns):
        di = self.data.get_data_index(index)
        key = self.data.get_model_tokenizer_key(index)

        horizontal_headers[key][di] = np.delete(horizontal_headers[key][di], columns, axis=0)
        vertical_headers[key][di] = np.delete(vertical_headers[key][di], rows, axis=0)    
        vertical_ids[key][di] = np.delete(vertical_ids[key][di], rows, axis=0)        
        data[key][di] = np.delete(data[key][di], rows, axis=-2)
        data[key][di] = np.delete(data[key][di], columns, axis=-1)

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids
    
    def fuse_rows(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, rows, index, fuse_key):
        di = self.data.get_data_index(index)
        key = self.data.get_model_tokenizer_key(index)

        rows_delete_first, rows_first = AnvnUtils.delete_first(rows)
        rows_merge = data[key][di][rows]
        rows_merge = AnvnUtils.get_fuse_op()[fuse_key](rows_merge, -2)
        data[key][di] = np.delete(data[key][di], rows_delete_first, axis=-2)
        data[key][di][rows_first] = rows_merge
        
        vertical_headers[key][di] = np.delete(vertical_headers[key][di], rows_delete_first, axis=0)
        ver_ids = vertical_ids[key][di][rows]
        ver_ids = AnvnUtils.flatten_list(ver_ids)
        vertical_ids[key][di] = np.delete(vertical_ids[key][di], rows_delete_first, axis=0)

        id = self.data.get_tokenizer(key).decode(ver_ids)
        vertical_headers[key][di][rows_first] = id
        vertical_ids[key][di][rows_first] = ver_ids

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids
    
    def fuse_columns(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, columns, fuse_key):
        di = self.data.get_data_index(index)
        key = self.data.get_model_tokenizer_key(index)

        columns_delete_first, columns_first = AnvnUtils.delete_first(columns)
        columns_merge = data[key][di][:,columns]
        columns_merge = AnvnUtils.get_fuse_op()[fuse_key](columns_merge, -1)
        data[key][di] = np.delete(data[key][di], columns_delete_first, axis=-1)
        data[key][di][:, columns_first] = columns_merge

        hors = horizontal_headers[key][di][columns]
        horizontal_headers[key][di] = np.delete(horizontal_headers[key][di], columns_delete_first, axis=0)
        horizontal_headers[key][di][columns_first] = ','.join(hors)

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids

class AnvnPoolerTableManagement(AnvnTableManagement):
    def __init__(self, data: AnvnTableData):
        super(AnvnPoolerTableManagement, self).__init__(data)

    def data2table(self):
        data, horizontal_headers, vertical_headers = super().data2table()
        table = AnvnTableWidget()
        table.itemSelectionChanged.connect(self.table_selection_func(table))
        table.data2table(data[self.data.get_model_tokenizer_key()], horizontal_headers[self.data.get_model_tokenizer_key()], vertical_headers, self.data.get_decimal_digit())
        self.add_table(table)
    
    def remove(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, rows, columns):
        key = self.data.get_model_tokenizer_key(index)

        horizontal_headers[key] = np.delete(horizontal_headers[key], columns, axis=0)
        data[key] = np.delete(data[key], columns, axis=-1)

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids
        
    def fuse_columns(self, data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids, index, columns, fuse_key):
        key = self.data.get_model_tokenizer_key(index)

        columns_delete_first, columns_first = AnvnUtils.delete_first(columns)
        columns_merge = data[key][:, columns]
        columns_merge = AnvnUtils.get_fuse_op()[fuse_key](columns_merge, -1)
        data = np.delete(data[key], columns_delete_first, axis=-1)
        data[key][:, columns_first] = columns_merge
        
        hors = horizontal_headers[key][columns]
        horizontal_headers[key] = np.delete(horizontal_headers[key], columns_delete_first, axis=0)
        horizontal_headers[key][columns_first] = ','.join(hors)

        return data, horizontal_headers, vertical_headers, horizontal_ids, vertical_ids
    
    def table_selection_func(self, table):
        def ts():
            rows, columns = table.get_selected()
            if len(columns) != 0 and len(rows) == 0:
                self.remove_but.setDisabled(False)
            else:
                self.remove_but.setDisabled(True)
            
            if len(columns) > 1:
                self.fuse_columns_but.setDisabled(False)
                self.fuse_cb.setDisabled(False)
            else:
                self.fuse_cb.setDisabled(True)
                self.fuse_columns_but.setDisabled(True)
        return ts 