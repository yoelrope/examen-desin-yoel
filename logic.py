from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from random import randint


CELL_SIZE = 20
GRID_SIZE = 20
WINDOW_SIZE = CELL_SIZE * GRID_SIZE


class SnakeGame:
    def __init__(self, widget):
        self.widget = widget

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)

        self.reset_game()

    def reset_game(self):
        self.snake = [
            QPoint(10, 10),
            QPoint(9, 10),
            QPoint(8, 10)
        ]

        self.direction = Qt.Key_Right
        self.food = self.generate_food()

        self.score = 0
        self.game_over = False

        self.timer.start(120)

    def generate_food(self):
        while True:
            point = QPoint(
                randint(0, GRID_SIZE - 1),
                randint(0, GRID_SIZE - 1)
            )

            if point not in self.snake:
                return point

    def change_direction(self, key):
        opposite = {
            Qt.Key_Up: Qt.Key_Down,
            Qt.Key_Down: Qt.Key_Up,
            Qt.Key_Left: Qt.Key_Right,
            Qt.Key_Right: Qt.Key_Left
        }

        if key in opposite:
            if opposite[key] != self.direction:
                self.direction = key

    def update_game(self):
        if self.game_over:
            return

        head = QPoint(self.snake[0])

        if self.direction == Qt.Key_Up:
            head.setY(head.y() - 1)

        elif self.direction == Qt.Key_Down:
            head.setY(head.y() + 1)

        elif self.direction == Qt.Key_Left:
            head.setX(head.x() - 1)

        elif self.direction == Qt.Key_Right:
            head.setX(head.x() + 1)

        # Colisiones bordes
        if (
            head.x() < 0 or
            head.y() < 0 or
            head.x() >= GRID_SIZE or
            head.y() >= GRID_SIZE
        ):
            self.end_game()
            return

        # Colisión consigo mismo
        if head in self.snake:
            self.end_game()
            return

        self.snake.insert(0, head)

        # Comer comida
        if head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.widget.update()

    def end_game(self):
        self.game_over = True
        self.timer.stop()
        self.widget.update()

    def draw_grid(self, painter):
        pen = QPen(QColor(55, 55, 55))
        pen.setWidth(1)

        painter.setPen(pen)

        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            painter.drawLine(x, 0, x, WINDOW_SIZE)

        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            painter.drawLine(0, y, WINDOW_SIZE, y)

    def draw_snake(self, painter):
        for index, part in enumerate(self.snake):

            x = part.x() * CELL_SIZE
            y = part.y() * CELL_SIZE

            # Cabeza más clara
            if index == 0:
                painter.setBrush(QColor(0, 255, 170))
            else:
                painter.setBrush(QColor(0, 200, 120))

            painter.setPen(Qt.NoPen)

            painter.drawRoundedRect(
                x + 2,
                y + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4,
                5,
                5
            )

    def draw_food(self, painter):
        painter.setBrush(QColor(255, 70, 70))
        painter.setPen(Qt.NoPen)

        x = self.food.x() * CELL_SIZE
        y = self.food.y() * CELL_SIZE

        painter.drawEllipse(
            x + 3,
            y + 3,
            CELL_SIZE - 6,
            CELL_SIZE - 6
        )

    def draw_score(self, painter):
        painter.setPen(QColor(255, 255, 255))

        font = QFont()
        font.setPointSize(12)
        font.setBold(True)

        painter.setFont(font)

        painter.drawText(10, 25, f"Score: {self.score}")

    def draw_game_over(self, painter):
        painter.setPen(QColor(255, 255, 255))

        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)

        painter.setFont(title_font)

        painter.drawText(
            self.widget.rect(),
            Qt.AlignCenter,
            "GAME OVER"
        )

        small_font = QFont()
        small_font.setPointSize(11)

        painter.setFont(small_font)

        painter.drawText(
            110,
            240,
            "Pulsa R para reiniciar"
        )

    def draw(self, event):
        painter = QPainter(self.widget)

        # Fondo oscuro moderno
        painter.fillRect(
            self.widget.rect(),
            QColor(25, 25, 25)
        )

        self.draw_grid(painter)
        self.draw_food(painter)
        self.draw_snake(painter)
        self.draw_score(painter)

        if self.game_over:
            self.draw_game_over(painter)