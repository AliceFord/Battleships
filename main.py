from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys


class Board(QGridLayout):
	def __init__(self, rows, columns, clicked):
		super(Board, self).__init__()

		self.buttons = []

		for i in range(rows):
			self.buttons.append([])
			for j in range(columns):
				button = QPushButton(" ")
				button.clicked.connect(lambda _, i=i, j=j: clicked(i, j))
				self.addWidget(button, i, j)
				self.buttons[i].append(button)

	def getButtons(self):
		return self.buttons

	def getButton(self, x, y):
		return self.buttons[x][y]

	def setButtonText(self, x, y, text):
		self.buttons[x][y].setText(text)


class MainWindow(QMainWindow):
	def __init__(self, setupCompleteFunction, swapPlayerFunction, player, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setupCompleteFunction = setupCompleteFunction
		self.playerSelectedLocations = 5
		self.setupMode = True

		mainWidget = QWidget()
		mainLayout = QVBoxLayout()
		mainLayout.setAlignment(Qt.AlignCenter)

		# Enemy board setup
		enemyBoardLabel = QLabel("Enemy Board")
		font = QFont()
		font.setPointSize(25)
		enemyBoardLabel.setFont(font)

		enemyBoardWidget = QWidget()
		self.enemyBoard = Board(8, 8, swapPlayerFunction)
		enemyBoardWidget.setLayout(self.enemyBoard)

		# User board setup
		userBoardLabel = QLabel(f"Your Board (Player {player})")
		font = QFont()
		font.setPointSize(25)
		userBoardLabel.setFont(font)

		userBoardWidget = QWidget()
		self.userBoard = Board(8, 8, self.setupButtonClicked)
		userBoardWidget.setLayout(self.userBoard)

		mainLayout.addWidget(enemyBoardLabel)
		mainLayout.addWidget(enemyBoardWidget)
		mainLayout.addWidget(userBoardLabel)
		mainLayout.addWidget(userBoardWidget)

		mainLayout.setAlignment(Qt.AlignTop)
		mainWidget.setLayout(mainLayout)

		self.setCentralWidget(mainWidget)
		self.setWindowTitle("Battleships")
		self.setGeometry(50, 50, 100, 100)
		self.show()

	def setupButtonClicked(self, x, y):
		self.playerSelectedLocations -= 1
		self.userBoard.setButtonText(x, y, "S")
		if self.playerSelectedLocations == 0:
			self.lockBoard(function=self.setupCompleteFunction)

	def lockBoard(self, topBoard=False, function=None):
		if topBoard:
			buttons = self.enemyBoard.getButtons()
			[button.setEnabled(False) for buttonList in buttons for button in buttonList]
		else:
			buttons = self.userBoard.getButtons()
			[button.setEnabled(False) for buttonList in buttons for button in buttonList]
		if function is not None:
			function()

	def unlockBoard(self, topBoard=False, function=None):
		if topBoard:
			buttons = self.enemyBoard.getButtons()
			[button.setEnabled(True) for buttonList in buttons for button in buttonList]
		else:
			buttons = self.userBoard.getButtons()
			[button.setEnabled(True) for buttonList in buttons for button in buttonList]
		if function is not None:
			function()


class Parent:
	def __init__(self):
		self.firstTime = True
		self.currentUser = 1
		self.p1FoundShips = 0
		self.p2FoundShips = 0
		app = QApplication(sys.argv)
		self.player1 = MainWindow(self.setupComplete, self.swapUser, "1")
		self.player1.lockBoard(True)
		self.player2 = MainWindow(self.setupComplete, self.swapUser, "2")
		self.player2.lockBoard(True)
		app.exec_()

	def setupComplete(self):
		if self.firstTime:
			self.firstTime = False
		else:
			self.player1.unlockBoard(True)

	def swapUser(self, i, j):
		if self.currentUser == 1:
			if self.player2.userBoard.getButton(i, j).text() == "S":
				self.player1.enemyBoard.setButtonText(i, j, "O")
				self.p1FoundShips += 1
			else:
				self.player1.enemyBoard.setButtonText(i, j, "X")
			self.player1.lockBoard(True)
			self.player2.unlockBoard(True)
			self.currentUser = 2
		elif self.currentUser == 2:
			if self.player1.userBoard.getButton(i, j).text() == "S":
				self.player2.enemyBoard.setButtonText(i, j, "O")
				self.p2FoundShips += 1
			else:
				self.player2.enemyBoard.setButtonText(i, j, "X")

			self.player1.unlockBoard(True)
			self.player2.lockBoard(True)
			self.currentUser = 1

		if self.p1FoundShips >= 5:
			msgBox = QMessageBox()
			msgBox.setText("Player 1 wins!")
			msgBox.exec_()
			self.player1.destroy()
			self.player2.destroy()
			sys.exit()
		elif self.p2FoundShips >= 5:
			msgBox = QMessageBox()
			msgBox.setText("Player 2 wins!")
			msgBox.exec_()
			self.player1.destroy()
			self.player2.destroy()
			sys.exit()


if __name__ == '__main__':
	Parent()
