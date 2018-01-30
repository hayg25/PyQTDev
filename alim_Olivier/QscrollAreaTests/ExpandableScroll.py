import sys
from PyQt4 import QtGui, QtCore

class Widget(QtGui.QWidget):
    """ Here we add more buttons, if the size of the buttons exceeds the size of the widget scrolling starts. """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.setLayout(self.vbox)

    def add_button(self):
        tmp = QtGui.QPushButton("...", self)
        self.vbox.addWidget(tmp)

class ScrollArea(QtGui.QScrollArea):
    """ This scroll area only handles one widget for which scrolling should be provided. """
    def __init__(self, parent=None):
        QtGui.QScrollArea.__init__(self, parent)

        self.w = Widget()
        self.setWidget(self.w)    #set the widget to provide scrolling for here

    def add_button(self):
        self.w.add_button()

class MainWindow(QtGui.QWidget):
    """ Use this widget to arrange the QScrollArea and the QPushButton. """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.vbox = QtGui.QVBoxLayout()
        self.scroll = ScrollArea(self)
        self.vbox.addWidget(self.scroll)

        self.plus = QtGui.QPushButton("button", self)
        self.connect(self.plus, QtCore.SIGNAL("clicked()"), self.add_button)
        self.vbox.addWidget(self.plus)

        self.setLayout(self.vbox)

    def add_button(self):
        self.scroll.add_button()

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())