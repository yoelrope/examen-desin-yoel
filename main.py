import sys
from PySide6.QtWidgets import QApplication
from ui_main import SnakeWindow


def main():
    app = QApplication(sys.argv)

    window = SnakeWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()