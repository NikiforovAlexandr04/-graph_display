import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt paint'
        self.left = 100
        self.top = 100
        self.width = 540
        self.height = 540
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

        delta = 20 #масштаб, количество делений вдоль оси

        qp = QPainter(self)
        qp.setPen(Qt.black)
        for i in range(540):
            qp.drawPoint(270, i)
            qp.drawPoint(i, 270)

        previous_points = 0
        points_x = []
        for i in range(101):
            points_x.append(delta - i*delta/50)

        points = []
        for i in points_x:
            pt_y = self.f(i)
            if abs(pt_y) < delta*3:
                points.append(self.convert_coords(i, pt_y, delta))

        for point in points:
            qp.drawPoint(point[0], point[1])
            if previous_points != 0:
                self.draw_line(qp, point[0], point[1], previous_points[0], previous_points[1])
            previous_points = point

        self.show_scale(delta, qp)

    #заданная функция
    def f(self, x):
        return x*x*x

    #преобразуем координаты из декартовых в экранные
    def convert_coords(self, x, y, delta):
        return int(x*540/delta) + 270, -int(y*540/delta) + 270

    #соединяем точки с помощью алгоритма
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

    #рисуем масштабные метки
    def show_scale(self, delta, qp):
        font = qp.font()
        font.setPointSize(8)
        qp.setFont(font)
        for i in range(21):
            cord = int(i*540/20)
            qp.drawPoint(268, cord)
            qp.drawPoint(269, cord)
            qp.drawPoint(271, cord)
            qp.drawPoint(272, cord)
            qp.drawPoint(cord, 268)
            qp.drawPoint(cord, 269)
            qp.drawPoint(cord, 271)
            qp.drawPoint(cord, 272)
            if i != 0 and i != 20: qp.drawText(cord - 10, 285, str(-delta/2 + i * delta / 20))
            if i != 0 and i != 20 and i != 10: qp.drawText(275, cord + 5, str(delta/2 - i * delta / 20))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
