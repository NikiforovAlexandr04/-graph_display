import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import random

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt paint'
        self.left = 100
        self.top = 100
        self.width = 540
        self.height = 380
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

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
        for i in range(380):
            qp.drawPoint(270, i)
        for i in range(540):
            qp.drawPoint(i, 190)
        previous_points = 0
        for i in range(-270, 270):
            pt = self.convert_coords(i, self.f(i))
            qp.drawPoint(pt[0], pt[1])
            if previous_points != 0:
                self.draw_line(qp, pt[0], pt[1], previous_points[0], previous_points[1])
            previous_points = pt

    def f(self, x):
        return x

    def convert_coords(self, x, y):
        return x + 270, -y + 190

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

        qp.drawPoint(x2, y2)
        while (x1 != x2 or y1 != y2):
            qp.drawPoint(x1, y1)
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
