import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow

def main():
    # Create the application instance
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
