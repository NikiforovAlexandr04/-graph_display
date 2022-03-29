import math
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


A = 0
B = 2


# заданная функция
def f(x):
    return math.sqrt(x) if x > 0 else 0


WIDTH = 720
POINTS = {}


def getHeight():
    points_x = []
    for i in range(101):
        points_x.append(B - i * B / 50)
    for x in points_x:
        POINTS[x] = f(x)
    max_y = max(POINTS.values())
    min_y = min(POINTS.values())
    step = WIDTH / (B - A)
    hgt = int((max_y - min_y) * step)
    return hgt if hgt < 1024 else 1024, min_y, max_y


def getAxis(height, min_y, max_y):
    axis_x = WIDTH / (B - A) * (0 - A)
    axis_y = height / (max_y - min_y)*(0-min_y)
    axis_y = axis_y if axis_y > 0 else 10
    axis_y = axis_y if axis_y < height else height
    return int(axis_x), int(axis_y)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt paint'
        self.left = 100
        self.top = 0
        self.width = WIDTH
        self.height = getHeight()[0]
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # Add paint widget and paint
        self.m = PaintWidget(self)
        self.m.move(0, 0)
        self.m.resize(self.width, self.height)

        self.show()


class PaintWidget(QWidget):

    def paintEvent(self, event):

        qp = QPainter(self)
        qp.setPen(Qt.black)

        height, min_y, max_y = getHeight()
        axis_x, axis_y = getAxis(height, min_y, max_y)

        for i in range(height):
            qp.drawPoint(axis_x, i)
        for i in range(WIDTH):
            qp.drawPoint(i, height - axis_y)

        previous_points = 0

        for x in POINTS:
            y = POINTS[x]
            y = y if abs(y) <= height else height + 10
            converted_pt = self.convert_coords(x, y, axis_x, axis_y, height)
            qp.drawPoint(converted_pt[0], converted_pt[1])
            if previous_points != 0:
                self.draw_line(qp, converted_pt[0], converted_pt[1], previous_points[0], previous_points[1])
            previous_points = converted_pt

    #преобразуем координаты из декартовых в экранные
    def convert_coords(self, x, y, axis_x, axis_y, height):
        coef = WIDTH/(B-A)
        cord_x = axis_x +coef*x
        cord_y = height - (axis_y + coef*y)
        return int(cord_x), int(cord_y)

    #соединяем точки с помощью алгоритма Брезенхема
    def draw_line(self, qp, x1, y1, x2, y2):
        delta_x = abs(x2 - x1)
        delta_y = abs(y2 - y1)
        if x1 < x2:
            sign_x = 1
        else:
            sign_x = -1
        if y1 < y2:
            sign_y = 1
        else:
            sign_y = -1
        error = delta_x - delta_y

        qp.drawPoint(int(x2), int(y2))

        while (x1 != x2 or y1 != y2):
            qp.drawPoint(int(x1), int(y1))
            error_2 = error * 2

            if error_2 > -delta_y:
                error -= delta_y
                x1 += sign_x

            if error_2 < delta_x:
                error += delta_x
                y1 += sign_y


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
