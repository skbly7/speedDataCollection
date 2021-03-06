import pyaudio
import wave
import time
from PyQt4 import QtGui
from PyQt4.QtCore  import *
from about import About
from rec import VoiceRec
from play import Play

class Gui(QtGui.QMainWindow,QtGui.QWidget):

	def __init__(self):
		super(Gui, self).__init__()
		self.initUI()
		self.line=0
		self.text=[]
		self.decode=""

	def initUI(self):

		self.vr = VoiceRec()
		self.pl = Play()
		self.vrThread = QThread()
		self.vr.moveToThread(self.vrThread)
		self.vrThread.started.connect(self.vr.record)

		openFile = QtGui.QAction(QtGui.QIcon('open.png'), '&Open', self)
		openFile.setShortcut('Ctrl+O')
		openFile.setStatusTip('Open new File')
		openFile.triggered.connect(self.showDialogOpen)

		exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QtGui.qApp.quit)

		utf_8 = QtGui.QAction('&UTF-8', self)
		utf_8.setStatusTip('utf-8')
		utf_8.triggered.connect(self.encodeUTF8)

		utf_16 = QtGui.QAction('&UTF-16', self)
		utf_16.setStatusTip('utf-16')
		utf_16.triggered.connect(self.encodeUTF16)

		about = QtGui.QAction('&About', self)
		about.setStatusTip('More About Voice Recorder')
		about.triggered.connect(self.showAbout)

		self.textEdit = QtGui.QTextEdit(self)
		self.textEdit.setGeometry(10,30,825,104)
		self.textEdit.setStyleSheet("QTextEdit {font-size: 14pt}")
		self.textEdit.setReadOnly(True)

		self.Open = QtGui.QPushButton('Open', self)
		self.Open.move(10,160)
		self.Open.clicked.connect(self.showDialogOpen)

		self.Record = QtGui.QPushButton('Record', self)
		self.Record.move(155,160)
		self.Record.clicked.connect(self.vrThread.start)

		self.Stop = QtGui.QPushButton('Stop', self)
		self.Stop.move(300,160)
		self.Stop.clicked.connect(self.stop)

		self.Play = QtGui.QPushButton('Play', self)
		self.Play.move(445,160)
		self.Play.clicked.connect(self.pl.play)

		self.Back = QtGui.QPushButton('Back', self)
		self.Back.move(590,160)
		self.Back.clicked.connect(self.showBack)

		self.Next = QtGui.QPushButton('Next', self)
		self.Next.move(735,160)
		self.Next.clicked.connect(self.showNext)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(openFile)
		fileMenu.addAction(exitAction)
		encodeMenu = menubar.addMenu('&Encoding')
		encodeMenu.addAction(utf_8)
		encodeMenu.addAction(utf_16)
		helpMenu = menubar.addMenu('&Help')
		helpMenu.addAction(about)

		self.setGeometry(200,200, 845, 200)
		self.setFixedSize(845 , 200)
		self.setWindowTitle('Voice Recorder')
		self.setWindowIcon(QtGui.QIcon('logo.png'))
		self.show()

	def showDialogOpen(self):
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home')
		if(fname!=""):
			del self.text[:]
			f = open(fname, 'r')
			for lines in f:
				self.text.append(lines)
			f.close
			if(self.decode!=""):
				self.textEdit.setText(self.text[self.line].decode(self.decode))
			else:
				self.textEdit.setText(self.text[self.line].decode('utf-8'))
			self.line=0

	def showNext(self):
		self.line+=1
		if(len(self.text)>self.line):
			if(self.decode!=""):
				self.textEdit.setText(self.text[self.line].decode(self.decode))
			else:
				self.textEdit.setText(self.text[self.line].decode('utf-8'))
		else:
			self.showDialogOpen()

	def showBack(self):
		self.line-=1
		if(len(self.text)>=self.line and self.line>=0):
			if(self.decode!=""):
				self.textEdit.setText(self.text[self.line].decode(self.decode))
			else:
				self.textEdit.setText(self.text[self.line].decode('utf-8'))
		else:
			self.showDialogOpen()

	def showAbout(self):
		self.popup1=About()
		self.popup1.exec_()

	def encodeUTF8(self):
		self.decode="utf-8"

	def encodeUTF16(self):
		self.decode="utf-16"

	def stop(self):
		self.vr.stop()
		self.vrThread.exit()
		self.vrThread.wait()
		self.vrThread.quit()