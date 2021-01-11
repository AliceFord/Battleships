from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import re
import sys


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.docks = []
		self.currentDock = 0

		mainWidget = QWidget()
		mainLayout = QGridLayout()

		ROWS = 10
		COLUMNS = 10

		

		for i in range(ROWS):
			for j in range(COLUMNS):
				button = QPushButton("")
				mainLayout.addWidget(button, i, j)

		mainLayout.setAlignment(Qt.AlignTop)
		mainWidget.setLayout(mainLayout)

		self.setCentralWidget(mainWidget)
		self.setWindowTitle("Auto Documenter")
		self.setGeometry(50, 50, 400, 400)
		self.show()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	app.exec_()
