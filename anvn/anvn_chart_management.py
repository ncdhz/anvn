from anvn_widget_utils import AnvnDockWidget, AnvnComboBox, AnvnOpButton, AnvnCloseButton
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from anvn_chart import AnvnChart
from anvn_chart_setting import AnvnChartSetting, AnvnChartSettingData

class AnvnChartManagement(QMainWindow):
    def __init__(self, data, title, parent=None):
        super().__init__()
        self.setting_data = AnvnChartSettingData()
        self.main_widget = AnvnDockWidget(title, parent, title_color='#2c2c2c', title_background='#f0f0f0')
        self.list_item = None
        self.data = data
        self.setStatusTip(title)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.main_widget)
        self.main_widget.set_title_double_clicked(self.__double_click_func)
        self.title_double_clicked_func = None
        self.close_func = None
        self.data_index = 0
        self.layer_index = 0
        self.head_index = 0
        self.chart_widget = QFrame()
        self.setObjectName('chart_widget')
        self.chart_layout = QVBoxLayout()
        self.chart_layout.setContentsMargins(0, 0, 0, 0)
        self.chart_widget.setLayout(self.chart_layout)
        self.data_layer_head_key = None
        self.current_chart = None
        self.all_charts = {
            AnvnChart.heatmap: self.heatmap,
        }
        self.data_layer_head_cb, self.down_but, self.data_layer_head_text, self.up_but = self.__init_chart_op()
        self.chart = AnvnChart()
        self.chart_layout.addWidget(self.chart)
        self.main_widget.setWidget(self.chart_widget)
        self.__set_style()
        if self.down_but is not None and self.up_but is not None:
            self.__refresh_data_layer_head()

    def set_list_item(self, item):
        self.list_item = item

    def set_setting_data(self, data):
        self.setting_data = data
        self.__refresh_chart()

    def get_key(self):
        return self.data.get_key()

    def set_title(self, title):
        self.main_widget.set_title(title)

    def __down_func(self):
        if self.data_layer_head_key == self.data.data_name:
            self.data_index -= 1
        elif self.data_layer_head_key == self.data.layer_name:
            self.layer_index -= 1
        else:
            self.head_index -= 1
        self.__refresh_data_layer_head()
        self.__refresh_chart()

    def __up_func(self):
        if self.data_layer_head_key == self.data.data_name:
            self.data_index += 1
        elif self.data_layer_head_key == self.data.layer_name:
            self.layer_index += 1
        else:
            self.head_index += 1
        self.__refresh_data_layer_head()
        self.__refresh_chart()

    def __refresh_chart(self):
        if self.current_chart is not None:
            self.all_charts[self.current_chart]()

    def __data_layer_head_func(self, text):
        self.data_layer_head_key = text
        self.__refresh_data_layer_head()


    def __refresh_data_layer_head(self):
        def refresh_but(index, dl):
            if index > 0:
                self.down_but.setDisabled(False)
                if index < dl - 1:
                    self.up_but.setDisabled(False)
                else:
                    self.up_but.setDisabled(True)
            else:
                self.down_but.setDisabled(True)
                self.up_but.setDisabled(False)

        if self.data_layer_head_key == self.data.data_name:
            self.data_layer_head_text.setText(str(self.data.data_num[self.data_index]))
            refresh_but(self.data_index, len(self.data.data_num))
        elif self.data_layer_head_key == self.data.layer_name:
            self.data_layer_head_text.setText(str(self.data.layers[self.layer_index]))
            refresh_but(self.layer_index, len(self.data.layers))
        else:
            self.data_layer_head_text.setText(str(self.data.heads[self.head_index]))
            refresh_but(self.head_index, len(self.data.heads))

    def heatmap(self, data=None):
        self.chart.heatmap(data)
        self.current_chart = AnvnChart.heatmap

    def setting(self):
        return AnvnChartSetting('Chart Setting', data=self.setting_data, ok_callback=self.set_setting_data)

    def __init_chart_op(self):
        spacing = 5
        op_frame = QFrame()
        op_frame.setObjectName('op_frame')
        layout = QHBoxLayout()

        AnvnOpButton(icon_name='setting', layout=layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.setting)
        AnvnOpButton(icon_name='heatmap', layout=layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.heatmap)
        

        items = []
        if self.__class__ != AnvnPoolerChartManagement:
            if self.data.data_num is not None and len(self.data.data_num) > 1:
                items.append(self.data.data_name)
            if self.data.layers is not None and len(self.data.layers) > 1:
                items.append(self.data.layer_name)
            if self.data.heads is not None and len(self.data.heads) > 1:
                items.append(self.data.head_name)


        data_layer_head_cb = None
        down_but = None
        data_layer_head_text = None
        up_but = None

        if len(items) > 0:
            self.data_layer_head_key = items[0]
            if len(items) > 1:
                data_layer_head_cb = AnvnComboBox(layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)
                data_layer_head_cb.addItems(items)
                data_layer_head_cb.currentTextChanged.connect(self.__data_layer_head_func)
        
            down_but = AnvnOpButton('#17abe3', '', 'down', layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__down_func)

            data_layer_head_text = QLabel()
            data_layer_head_text.setObjectName('data_layer_head_text')
            layout.addWidget(data_layer_head_text)

            up_but = AnvnOpButton('#17abe3', '', 'up', layout, alignment=Qt.AlignmentFlag.AlignLeft, spacing=spacing)(self.__up_func)
        
        layout.addStretch(0)
        
        close = AnvnCloseButton()(self.__close_func)
        layout.addWidget(close)

        op_frame.setLayout(layout)
        self.chart_layout.addWidget(op_frame)
        return data_layer_head_cb, down_but, data_layer_head_text, up_but

    def set_close(self, func):
        self.close_func = func

    def __close_func(self):
        if self.close_func is not None:
            self.close_func()

    def clear(self):
        if not self.main_widget.isFloating():
            widget = QWidget()
            widget.setFixedHeight(0)
            self.main_widget.setWidget(widget)
            if self.list_item is not None:
                self.list_item.setSizeHint(self.sizeHint())

    def open(self):
        self.main_widget.setWidget(self.chart_widget)
        self.main_widget.resize(600, 600)
        if self.list_item is not None:
            self.list_item.setSizeHint(self.sizeHint())

    def reduction_event(self, func):
        self.main_widget.set_reduction_func(lambda : func(self))

    def floating_event(self, func):
        self.main_widget.set_floating_func(lambda: func(self))

    def set_title_double_clicked(self, func):
        self.title_double_clicked_func = func

    def __set_style(self):
        self.setStyleSheet('''
            #chart_widget {
                margin: 10px;
            }
            #data_layer_head_text {
                color: #17abe3;
            }
            #op_frame {
                border: 1px solid #dbdbdb;
                border-radius: 5px;
                margin: 10px;
            }
        ''')

    def __double_click_func(self):
        if self.title_double_clicked_func is not None:
            self.title_double_clicked_func(self)


class AnvnLastHiddenStateChartManagement(AnvnChartManagement):
    def __init__(self, data, title, parent=None):
        super().__init__(data, title, parent)
    
    def setting(self):
        setting = super().setting()
        setting.set_heatmap_head_disabled(True)
        setting.set_heatmap_layer_disabled(True)
        setting.init_chart_op()
        setting.show()

    def heatmap(self, data=None):
        super().heatmap(self.data.data[self.data_index])

class AnvnPoolerChartManagement(AnvnChartManagement):
    def __init__(self, data, title, parent=None):
        super().__init__(data, title, parent)
    
    def setting(self):
        setting = super().setting()
        setting.set_heatmap_head_disabled(True)
        setting.set_heatmap_layer_disabled(True)
        setting.init_chart_op()
        setting.show()

    def heatmap(self, data=None):
        super().heatmap(self.data.data)

class AnvnHiddenStatesChartManagement(AnvnChartManagement):
    def __init__(self, data, title, parent=None):
        super().__init__(data, title, parent)

    def setting(self):
        setting = super().setting()
        setting.set_heatmap_head_disabled(True)
        setting.init_chart_op()
        setting.show()

    def heatmap(self, data=None):
        data = self.data.data[self.data_index]
        if self.setting_data.fuse_option[self.setting_data.layer_fuse] is not None:
            data = self.setting_data.fuse_option[self.setting_data.layer_fuse](data, 0)
        else:
            data = data[self.layer_index]

        super().heatmap(data)

class AnvnAttentionsChartManagement(AnvnChartManagement):
    def __init__(self, data, title, parent=None):
        super().__init__(data, title, parent)

    def setting(self):
        setting = super().setting()
        setting.init_chart_op()
        setting.show()

    def heatmap(self, data=None):
        data = self.data.data[self.data_index]
        if self.setting_data.fuse_option[self.setting_data.layer_fuse] is not None:
            data = self.setting_data.fuse_option[self.setting_data.layer_fuse](data, 0)
        else:
            data = data[self.layer_index]

        if self.setting_data.fuse_option[self.setting_data.head_fuse] is not None:
            data = self.setting_data.fuse_option[self.setting_data.head_fuse](data, 0)
        else:
            data = data[self.head_index]
        super().heatmap(data)
