from anvn_widget_utils import AnvnComboBox, AnvnOpButton, AnvnDialog, AnvnFrame, AnvnInformationWidget
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QTabWidget
import numpy as np

class AnvnChartSettingData:
    def __init__(self):
        self.layer_fuse = 'none'
        self.head_fuse = 'none'
        self.fuse_option = {'none': None, 'min': np.min, 'max': np.max, 'mean': np.mean, 'median': np.median, 'sum': np.sum}

class AnvnChartSetting(AnvnDialog):
    def __init__(self, title, data: AnvnChartSettingData, ok_callback=None, w=600, h=600, parent=None):
        super().__init__(title, w, h, parent)
        self.data = data
        self.ok_callback = ok_callback
        self.heatmap_head_disabled = False
        self.heatmap_layer_disabled = False
        self.main_layout = QVBoxLayout()
        self.chart_op_tab = QTabWidget()
        self.main_layout.addWidget(self.chart_op_tab)
        self.__init_ok_cancel_but()
        self.setLayout(self.main_layout)
        self.__set_style()

    def set_heatmap_head_disabled(self, disabled):
        self.heatmap_head_disabled = disabled
    
    def set_heatmap_layer_disabled(self, disabled):
        self.heatmap_layer_disabled = disabled

    def __set_style(self):
        self.chart_op_tab.setStyleSheet('''
            QTabWidget {
                border: 1px solid #e0e0e0;
            }
        ''')
    
    def init_chart_op(self):
        self.__init_heatmap_tab()

    def __heatmap_layer_cb_changed(self, text):
        self.data.layer_fuse = text

    def __heatmap_head_cb_changed(self, text):
        self.data.head_fuse = text

    def __init_heatmap_tab(self):
        heatmap_frame = QFrame()
        layout = QVBoxLayout()
        layer_and_head = AnvnInformationWidget("Layer and Head:")
        layer_and_head_layout = QHBoxLayout()

        layer_and_head_layout.addWidget(QLabel("Layer: "))
        layer_cb = AnvnComboBox(layer_and_head_layout)
        layer_cb.addItems(self.data.fuse_option.keys())
        layer_cb.setCurrentText(self.data.layer_fuse)
        layer_cb.currentTextChanged.connect(self.__heatmap_layer_cb_changed)
        layer_cb.setDisabled(self.heatmap_layer_disabled)
        

        layer_and_head_layout.addWidget(QLabel("Head: "))
        head_cb = AnvnComboBox(layer_and_head_layout)
        head_cb.addItems(self.data.fuse_option.keys())
        head_cb.setCurrentText(self.data.head_fuse)
        head_cb.currentTextChanged.connect(self.__heatmap_head_cb_changed)
        head_cb.setDisabled(self.heatmap_head_disabled)

        layer_and_head.add_layout(layer_and_head_layout)
        layer_and_head_layout.addStretch(0)
        layout.addWidget(layer_and_head)
        
        layout.addStretch(0)
        heatmap_frame.setLayout(layout)
        self.chart_op_tab.addTab(heatmap_frame, 'Heatmap')

    def __ok_func(self):
        self.__apply_func()
        self.close()

    def __apply_func(self):
        if self.ok_callback is not None:
            self.ok_callback(self.data)

    def __init_ok_cancel_but(self):
        frame = AnvnFrame(self)
        layout = QHBoxLayout()
        layout.addStretch(0)
        AnvnOpButton('#17abe3', 'OK', 'ok', layout)(self.__ok_func)
        AnvnOpButton('#eeb174', 'Apply', 'apply', layout)(self.__apply_func)
        AnvnOpButton('#d81e06', 'Cancel', 'cancel', layout)(lambda: {
            self.close()
        })
        frame.setLayout(layout)
        self.main_layout.addWidget(frame)