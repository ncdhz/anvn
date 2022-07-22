import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class AnvnChart(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.main_layout.addWidget(self.canvas)
        self.setLayout(self.main_layout)

    def run(self):
        ax = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
        ax.plot([1,2,3,4,5])
        self.canvas.draw()
