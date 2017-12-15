#!/usr/bin/env python
# -*- coding: utf-8 *-

import sys
import os

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import *

app = QtGui.QApplication(sys.argv)

class MyDialog(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Alim_IHM.ui"), self)
    # self.comboBox.currentIndexChanged.connect(self.updateList)
    self.comboBox.currentIndexChanged.connect(self.updateTable)
    self.comboBox.clear()
    self.comboBox.insertItems(0,self.getFilters())
    # self.updateList()
    self.updateTable()
    pass

  def updateList(self):
     # envoi de la liste des elements
    items = self.getListItems()
    text_filter = str(self.comboBox.currentText())
    self.listWidget.clear()
    # If "All" is used, no filter is applied
    self.listWidget.insertItems(0,[text for text in items if text_filter in text + "All"])
    pass


  def updateTable(self):
    print('updateTable')
     # envoi de la liste des elements
    items = self.getListItems()
    # filtre venant du choix du combobox
    text_filter = str(self.comboBox.currentText())
    # nettoyage de la zone ou on va ecrire
    self.tableWidget.clear()
    # If "All" is used, no filter is applied
    # cette methode n'existe pas : il faut trouver un equivalent
    # self.tableWidget.insertItems(0,[text for text in items if text_filter in text + "All"])
    k=-1
    for text in items:
        if text_filter in text+"All":
            k+=1
            print k,text
            self.tableWidget.setItem(k,0,QtGui.QTableWidgetItem(text))
            self.tableWidget.setItem(k,1,QtGui.QTableWidgetItem('koko'))
    pass



  def getFilters(self):
    # Write here your own method to retrieve the filters
    return ["Dipole", "Quad", "Sext", "All"]

  def getListItems(self):
    # Write here your own method to retrieve the list values
    return ["Quad01", "Quad02","Quad03", "Quad04","Quad05", "Quad06", "Dipole01", "Dipole02", "Dipole03","Sext01","Sext02","Setx03"]

myDialog = MyDialog()
myDialog.show()
sys.exit(app.exec_())
