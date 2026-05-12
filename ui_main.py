from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from logic import SnakeGame, WINDOW_SIZE


class SnakeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake MVC - PySide6")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)

        self.game = SnakeGame(self)

    def paintEvent(self, event):
        self.game.draw(event)

    def keyPressEvent(self, event):
        self.game.change_direction(event.key())

        if event.key() == Qt.Key_R and self.game.game_over:
            self.game.reset_game()