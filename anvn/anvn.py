import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QDesktopServices, QIcon
from resources import *
from menu_tool import AnvnMenu, AnvnToolBar
from widget import AnvnTabWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setMinimumSize(1100, 600)
        self.setWindowIcon(QIcon(':/logo'))
        self.anvn_tab_widget = AnvnTabWidget(self)
        self.anvn_menu = AnvnMenu(self, self.anvn_tab_widget)
        self.anvn_tool_bar = AnvnToolBar(self, self.anvn_tab_widget)
        self.setCentralWidget(self.anvn_tab_widget)
        self.status_bar_init()

    def status_bar_init(self):
        self.statusBar().showMessage('Ready Go !!!')

# Start program
def main():
    app = QApplication(sys.argv)    
    main_window = MainWindow()
    main_window.setWindowTitle('ANVN')
    main_window.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())

