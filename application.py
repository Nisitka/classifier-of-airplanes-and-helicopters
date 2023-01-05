from PyQt5.QtCore import QObject, pyqtSignal

from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5 import QtGui, QtWidgets
import guiUI  # конвертированный файл дизайна

import datetime

class gui(QtWidgets.QWidget, guiUI.Ui_Form):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле guiUI.py
        super().__init__()
        QObject.__init__(self)
        # для инициализации нашего дизайна
        self.setupUi(self)

        # настройки визула
        self.setWindowTitle("client-camera")


from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject

from PyQt5.QtGui import QImage, QPixmap, QColor
class Core(QObject):

    def __init__(self, argv):
        QObject.__init__(self)
        self.__app = QApplication(argv)

        self.appGui = gui()

    # запуск приложения
    def run(self):
        self.appGui.show()

        self.__app.exec_()


import sys  # sys нужен для передачи argv в QApplication

if __name__ == '__main__':
    # создание и запуск приложения
    cameraClient = Core(sys.argv)
    cameraClient.run()