from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from widget_utils import AnvnOpButton, AnvnTableWidget, AnvnComboBox
from PyQt5.QtCore import Qt
from anvn_utils import AnvnUtils
import numpy as np

class AnvnTableManagement(QWidget):
    def __init__(self, key, digit=5, tokenizer=None) -> None:
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.current_index = 0
        self.current_data = []
        self.key = key
        self.digit = digit
        self.data_num = None
        self.data = None
        self.layers = None
        self.heads = None
        self.vertical_headers = None
        self.horizontal_headers = None
        self.vertical_ids = None
        self.horizontal_ids = None
        self.change_event_callback = None
        self.tokenizer = tokenizer
        self.merge_option = {'min': np.min, 'max': np.max, 'mean': np.mean, 'median': np.median, 'sum': np.sum}
        self.merge_key = 'mean'
        self.remove_but, self.merge_cb, self.merge_but = self.__init_table_op()
        self.table_widget = AnvnTableWidget()
        self.table_widget.itemSelectionChanged.connect(self.table_clicked)
        self.main_layout.addWidget(self.table_widget)

    def get_vertical_headers(self):
        return self.vertical_headers
    
    def get_horizontal_headers(self):
        return self.horizontal_headers

    def get_data(self):
        return self.data

    def __remove_func(self):
        self.__refresh_data()
        self.remove_func()
        self.data2table()
        if self.change_event_callback is not None:
            self.change_event_callback()

    def change_event(self, callback):
        self.change_event_callback = callback

    def remove_func(self):
        pass
    
    def __merge_func(self):
        self.__refresh_data()
        self.merge_func()
        self.data2table()
        if self.change_event_callback is not None:
            self.change_event_callback()
    
    def merge_func(self):
        pass

    def __init_table_op(self):
        layout = QHBoxLayout()

        remove_but = AnvnOpButton('#d81e06', 'Remove', 'remove', layout,
                                  alignment=Qt.AlignmentFlag.AlignLeft)(self.__remove_func)
        remove_but.setDisabled(True)

        merge_cb = AnvnComboBox(layout, alignment=Qt.AlignmentFlag.AlignLeft)
        merge_cb.addItems(self.merge_option.keys())
        merge_cb.setCurrentText(self.merge_key)
        merge_cb.setDisabled(True)
        merge_cb.currentTextChanged.connect(self.__merge_type_func)

        merge_but = AnvnOpButton('#17abe3', 'Merge', 'merge', layout, alignment=Qt.AlignmentFlag.AlignLeft)(self.__merge_func)
        merge_but.setDisabled(True)
        
        layout.addStretch(0)
        self.main_layout.addLayout(layout)
        return remove_but, merge_cb, merge_but

    def __merge_type_func(self, text):
        if text != self.merge_key:
            self.merge_key = text

    def set_digit(self, digit):
        self.digit = digit
        self.data2table()

    def get_digit(self):
        return self.digit

    def get_key(self):
        return self.key

    def get_data_num(self):
        return self.data_num

    def get_layers(self):
        return self.layers

    def get_heads(self):
        return self.heads

    def is_start(self):
        return self.current_index == 0

    def is_end(self):
        return self.current_index == len(self.current_data) - 1

    def revoke(self):
        if self.is_start():
            return False
        self.current_index -= 1
        self.refresh_data()
        self.data2table()
        return True

    def forward(self):
        if self.is_end():
            return False
        self.current_index += 1
        self.refresh_data()
        self.data2table()
        return True

    def __refresh_data(self):
        for _ in range(self.current_index + 1, len(self.current_data)):
            del self.current_data[-1]
        self.refresh_data()

    def refresh_data(self):
        pass

    def data2table(self):
        pass

    def table_clicked(self):
        rows, columns = self.table_widget.get_selected()
        if len(rows) > 1 or len(columns) > 1:
            self.merge_but.setDisabled(False)
            self.merge_cb.setDisabled(False)
        else:
            self.merge_cb.setDisabled(True)
            self.merge_but.setDisabled(True)
        
        if (len(rows) == 0 and len(columns) == 0) or self.table_widget.columnCount() == len(columns) or self.table_widget.rowCount() == len(rows):
            self.remove_but.setDisabled(True)
        else:
            self.remove_but.setDisabled(False)
        
    def delete_index_after(self):
        self.current_data = self.current_data[:self.current_index + 1]

class AnvnAttentionTableManagement(AnvnTableManagement):
    def __init__(self, data, ots, iis, data_num, layers, heads, key, digit, tokenizer):
        super(AnvnAttentionTableManagement, self).__init__(key, digit, tokenizer)
        self.data_num = data_num
        self.layers = layers
        self.heads = heads
        self.data, self.horizontal_headers, self.vertical_headers, self.horizontal_ids, self.vertical_ids = AnvnUtils.deepcopy(data, ots, ots, iis, iis)
        self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.horizontal_ids, self.vertical_ids, 0, 0, 0))

        self.data2table()

    def remove_func(self):
        _, _, _, _, _, di, li, hi = self.current_data[self.current_index]
        rows, columns = self.table_widget.get_selected()
        for i, row in enumerate(rows):
            del self.vertical_headers[di][row - i]
            del self.vertical_ids[di][row - i]

        for i, column in enumerate(columns):
            del self.horizontal_headers[di][column - i]
            del self.horizontal_ids[di][column - i]

        for layer in self.layers:
            for head in self.heads:
                dlh = self.data[di][layer][head]
                for i, row in enumerate(rows):
                    del dlh[row - i]
                for i, column in enumerate(columns):
                    for j in range(len(dlh)):
                        del dlh[j][column - i]

        self.current_index += 1
        self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.horizontal_ids, self.vertical_ids, di, li, hi))
    
    def merge_func(self):
        _, _, _, _, _, di, li, hi = self.current_data[self.current_index]
        rows, columns = self.table_widget.get_selected()
        if len(rows) > 1:
            ver_ids = []
            for i, row in enumerate(rows):
                del self.vertical_headers[di][row - i]
                rid = self.vertical_ids[di][row - i]
                if isinstance(rid, list):
                    ver_ids.extend(rid)
                else:
                    ver_ids.append(rid)
                del self.vertical_ids[di][row - i]
            id = self.tokenizer.decode(ver_ids)
            self.vertical_headers[di].insert(rows[0], id)
            self.vertical_ids[di].insert(rows[0], ver_ids)
            
            for layer in self.layers:
                for head in self.heads:
                    row_merge = []
                    dlh = self.data[di][layer][head]
                    for i, row in enumerate(rows):
                        row_merge.append(dlh[row - i])
                        del dlh[row - i]
                    row_m = self.merge_option[self.merge_key](row_merge, 0).tolist()
                    dlh.insert(rows[0], row_m)
                    
        if len(columns) > 1:
            hor_ids = []
            for i, column in enumerate(columns):
                del self.horizontal_headers[di][column - i]
                rid = self.horizontal_ids[di][column - i]
                if isinstance(rid, list):
                    hor_ids.extend(rid)
                else:
                    hor_ids.append(rid)
                del self.horizontal_ids[di][column - i]
            id = self.tokenizer.decode(hor_ids)
            self.horizontal_headers[di].insert(columns[0], id)
            self.horizontal_ids[di].insert(columns[0], hor_ids)

            for layer in self.layers:
                for head in self.heads:
                    dlh = self.data[di][layer][head]
                    col_merge = []
                    for i, column in enumerate(columns):
                        c_merge = []
                        for j in range(len(dlh)):
                            c_merge.append(dlh[j][column - i])
                            del dlh[j][column - i]
                        col_merge.append(c_merge)
                    col_m = self.merge_option[self.merge_key](col_merge, 0).tolist()
                    for j in range(len(dlh)):
                        dlh[j].insert(columns[0], col_m[j])

        self.current_index += 1
        self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.horizontal_ids, self.vertical_ids, di, li, hi))

    def refresh_data(self):
        self.data, self.horizontal_headers, self.vertical_headers, self.horizontal_ids, self.vertical_ids, _, _, _ = AnvnUtils.deepcopy(*self.current_data[self.current_index])

    def data2table(self):
        data, horizontal_headers, vertical_headers, _, _, di, li, hi = self.current_data[self.current_index]
        self.table_widget.data2table(
            data[di][li][hi], horizontal_headers[di], vertical_headers[di], self.digit)

class AnvnStateTableManagement(AnvnTableManagement):
    def __init__(self, data, ots, iis, data_num, layers, key, digit, tokenizer):
        super(AnvnStateTableManagement, self).__init__(key, digit, tokenizer)
        self.data_num = data_num
        self.layers = layers
        self.data, self.vertical_headers, self.vertical_ids = AnvnUtils.deepcopy(data, ots, iis)
        if self.layers is None:
            self.horizontal_headers = AnvnUtils.n_range_str(len(self.data_num), 1, len(data[0][0]) + 1)
            self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.vertical_ids, 0))
        else:
            self.horizontal_headers = AnvnUtils.n_range_str(len(self.data_num), 1, len(data[0][0][0]) + 1)
            self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.vertical_ids, 0, 0))
        self.data2table()

    def refresh_data(self):
        if self.layers is None:
            self.data, self.horizontal_headers, self.vertical_headers, self.vertical_ids, _ = AnvnUtils.deepcopy(*self.current_data[self.current_index])
        else:
            self.data, self.horizontal_headers, self.vertical_headers, self.vertical_ids, _, _ = AnvnUtils.deepcopy(*self.current_data[self.current_index])

    def remove_func(self):
        rows, columns = self.table_widget.get_selected()
        if self.layers is None:
            _, _, _, _, di = self.current_data[self.current_index]
        else:
            _, _, _, _, di, li = self.current_data[self.current_index]

        for i, column in enumerate(columns):
            del self.horizontal_headers[di][column - i]
            
        for i, row in enumerate(rows):
            del self.vertical_headers[di][row - i]
            del self.vertical_ids[di][row - i]

        if self.layers is not None:
            for layer in self.layers:
                dlh = self.data[di][layer]
                for i, row in enumerate(rows):
                    del dlh[row - i]
                for i, column in enumerate(columns):
                    for j in range(len(dlh)):
                        del dlh[j][column - i]
        else:
            dlh = self.data[di]
            for i, row in enumerate(rows):
                del dlh[row - i]
            for i, column in enumerate(columns):
                for j in range(len(dlh)):
                    del dlh[j][column - i]

        self.current_index += 1
        if self.layers is None:
            self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.vertical_ids, di))
        else:
            self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.vertical_ids, di, li))

    def merge_func(self):
        rows, columns = self.table_widget.get_selected()
        if self.layers is None:
            _, _, _, _, di = self.current_data[self.current_index]
        else:
            _, _, _, _, di, li = self.current_data[self.current_index]

        if len(rows) > 1:
            ver_ids = []
            for i, row in enumerate(rows):
                del self.vertical_headers[di][row - i]
                rid = self.vertical_ids[di][row - i]
                if isinstance(rid, list):
                    ver_ids.extend(rid)
                else:
                    ver_ids.append(rid)
                del self.vertical_ids[di][row - i]
            id = self.tokenizer.decode(ver_ids)
            self.vertical_headers[di].insert(rows[0], id)
            self.vertical_ids[di].insert(rows[0], ver_ids)

            if self.layers is not None:
                for layer in self.layers:
                    row_merge = []
                    dlh = self.data[di][layer]
                    for i, row in enumerate(rows):
                        row_merge.append(dlh[row - i])                        
                        del dlh[row - i]
                    dlh.insert(rows[0], self.merge_option[self.merge_key](row_merge, 0).tolist())
            else:
                row_merge = []
                dlh = self.data[di]
                for i, row in enumerate(rows):
                    row_merge.append(dlh[row - i])
                    del dlh[row - i]
                dlh.insert(rows[0], self.merge_option[self.merge_key](row_merge, 0).tolist())

        if len(columns) > 1:
            hors = []
            for i, column in enumerate(columns):
                hors.append(self.horizontal_headers[di][column - i])
                del self.horizontal_headers[di][column - i]
            self.horizontal_headers[di].insert(columns[0], ','.join(hors))

            if self.layers is not None:
                for layer in self.layers:
                    column_merge = []
                    dlh = self.data[di][layer]
                    for i, column in enumerate(columns):
                        c_merge = []
                        for j in range(len(dlh)):
                            c_merge.append(dlh[j][column - i])
                            del dlh[j][column - i]
                        column_merge.append(c_merge)
                    col_m = self.merge_option[self.merge_key](column_merge, 0).tolist()
                    for j in range(len(dlh)):
                        dlh[j].insert(columns[0], col_m[j])                    
            else:
                column_merge = []
                dlh = self.data[di]
                for i, column in enumerate(columns):
                    c_merge = []
                    for j in range(len(dlh)):
                        c_merge.append(dlh[j][column - i])
                        del dlh[j][column - i]
                    column_merge.append(c_merge)
                col_m = self.merge_option[self.merge_key](column_merge, 0).tolist()
                for j in range(len(dlh)):
                    dlh[j].insert(columns[0], col_m[j])
        
        self.current_index += 1
        if self.layers is None:
            self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.vertical_ids, di))
        else:
            self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.vertical_ids, di, li))
            
    def data2table(self):
        if self.layers is None:
            data, horizontal_headers, vertical_headers, _, di = self.current_data[self.current_index]
            self.table_widget.data2table(data[di], horizontal_headers[di], vertical_headers[di], self.digit)
        else:
            data, horizontal_headers, vertical_headers, _, di, li = self.current_data[self.current_index]
            self.table_widget.data2table(data[di][li], horizontal_headers[di], vertical_headers[di], self.digit)

class AnvnPoolerTableManagement(AnvnTableManagement):
    def __init__(self, data, data_num, key, digit):
        super(AnvnPoolerTableManagement, self).__init__(key, digit)
        self.data_num = data_num
        self.data, self.vertical_headers = AnvnUtils.deepcopy(data, data_num)
        self.vertical_headers = [str(i) for i in self.vertical_headers]
        self.horizontal_headers = AnvnUtils.range_str(1, len(data[0]) + 1)
        self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers))
        self.data2table()

    def refresh_data(self):
        self.data, self.horizontal_headers, _ = AnvnUtils.deepcopy(*self.current_data[self.current_index]) 

    def remove_func(self):
        _, columns = self.table_widget.get_selected()
        for i, column in enumerate(columns):
            del self.horizontal_headers[column - i]
            for j in range(len(self.data_num)):
                del self.data[j][column - i]
    
        self.__add_current_data()

    def __add_current_data(self):
        self.current_index += 1
        self.current_data.append(AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers))

    def data2table(self):
        data, horizontal_header, vertical_header = self.current_data[self.current_index]
        self.table_widget.data2table(data, horizontal_header, vertical_header , self.digit)

    def merge_func(self):
        _, colums = self.table_widget.get_selected()
        column_merge = []
        hors = []
        for i, column in enumerate(colums):
            c_merge = []
            hors.append(self.horizontal_headers[column - i])
            del self.horizontal_headers[column - i]
            for j in range(len(self.data_num)):
                c_merge.append(self.data[j][column - i])
                del self.data[j][column - i]
            column_merge.append(c_merge)
        col_m = self.merge_option[self.merge_key](column_merge, 0).tolist()
        
        for j in range(len(self.data_num)):
            self.data[j].insert(colums[0], col_m[j])
        self.horizontal_headers.insert(colums[0], ','.join(hors))

        self.__add_current_data()

    def table_clicked(self):
        rows, columns = self.table_widget.get_selected()
        if len(columns) != 0 and len(rows) == 0:
            self.remove_but.setDisabled(False)
        else:
            self.remove_but.setDisabled(True)
        
        if len(columns) > 1:
            self.merge_but.setDisabled(False)
            self.merge_cb.setDisabled(False)
        else:
            self.merge_cb.setDisabled(True)
            self.merge_but.setDisabled(True)
