import sys
from PyQt5.QtWidgets import QApplication
from anvn_main_window import AnvnMainWindow

# Start program
def main():
    app = QApplication(sys.argv)    
    main_window = AnvnMainWindow()
    main_window.setWindowTitle('ANVN')
    main_window.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
