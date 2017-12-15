# The following tells SIP (the system that binds Qt's C++ to Python)
# to return Python native types rather than QString and QVariant
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)


from PyQt4 import QtCore, QtGui

class TableModel(QtCore.QAbstractTableModel):
    """
    A simple 5x4 table model to demonstrate the delegates
    """
    def rowCount(self, parent=QtCore.QModelIndex()): return 5
    def columnCount(self, parent=QtCore.QModelIndex()): return 4

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid(): return None
        if not role==QtCore.Qt.DisplayRole: return None
        return "{0:02d}".format(index.row())


class ComboDelegate(QtGui.QItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent):

        QtGui.QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):

        self.combo = QtGui.QComboBox(self.parent())
        self.connect(self.combo, QtCore.SIGNAL("currentIndexChanged(int)"), self.parent().currentIndexChanged)

        li = []
        li.append("Zero")
        li.append("One")
        li.append("Two")
        li.append("Three")
        li.append("Four")
        li.append("Five")

        self.combo.addItems(li)

        if not self.parent().indexWidget(index):
            self.parent().setIndexWidget(
                index,
                self.combo
            )

class TableView(QtGui.QTableView):
    """
    A simple table to demonstrate the QComboBox delegate.
    """
    def __init__(self, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)

        # Set the delegate for column 0 of our table
        # self.setItemDelegateForColumn(0, ButtonDelegate(self))
        self.setItemDelegateForColumn(0, ComboDelegate(self))

    @QtCore.pyqtSlot()
    def currentIndexChanged(self, ind):
        print "Combo Index changed {0} {1} : {2}".format(ind, self.sender().currentIndex(), self.sender().currentText())

if __name__=="__main__":
    from sys import argv, exit

    class Widget(QtGui.QWidget):
        """
        A simple test widget to contain and own the model and table.
        """
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)

            l=QtGui.QVBoxLayout(self)
            self._tm=TableModel(self)
            self._tv=TableView(self)
            self._tv.setModel(self._tm)
            l.addWidget(self._tv)

    a=QtGui.QApplication(argv)
    w=Widget()
    w.show()
    w.raise_()
    exit(a.exec_())
