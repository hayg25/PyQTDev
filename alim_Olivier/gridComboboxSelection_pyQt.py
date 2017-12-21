#!/usr/bin/env python
# -*- coding: utf-8 *-

import sys
import os
import taurus

from taurus.qt.qtgui.button import TaurusCommandButton
from taurus.qt.qtgui.display import TaurusLabel

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import *

app = QtGui.QApplication(sys.argv)

class MyDialog(QtGui.QWidget):


  def __init__(self):
    QtGui.QWidget.__init__(self)
    uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gridComboboxSelection_pyQt_layout.ui"), self)
    self.contenu = QtGui.QWidget()
    self.gridLayout = QtGui.QGridLayout()
    self.contenu.setLayout(self.gridLayout)
    self.readFileAlim()
    self.comboBox.currentIndexChanged.connect(self.updateList)
    self.comboBox.currentIndexChanged.connect(self.updateTable)
    self.comboBox.clear()
    self.comboBox.insertItems(0, self.getFilters())
    self.updateList()
    self.updateTable()

  def updateTable(self):
    # filtre venant du choix du combobox
	# Recherche dans le dictionnaire
    text_filter = filters.get(str(self.comboBox.currentText()))
    # nettoyage de la zone a ecrire
    #self.clearLayout(self.gridLayout)
	# Header du tableau a ecrire après chaque .clear
    #self.tableWidget.setHorizontalHeaderLabels(['Names','Current','Voltage'])
    # If "All" is used, no filter is applied
    # cette methode n'existe pas : il faut trouver un equivalent
    # self.tableWidget.insertItems(0,[text for text in items if text_filter in text + "All"])
    k=-1
    for device in DeviceList:
        if text_filter in device.nom+"All":
            k+=1
            self.gridLayout.addWidget(device.labelDevice, k, 0)
            self.gridLayout.addWidget(device.afficheurCurrent, k, 1)
            self.gridLayout.addWidget(device.afficheurVoltage, k, 2)
            self.gridLayout.addWidget(device.commandButtonSwitch, k, 3)
    self.scrollArea.setWidget(self.contenu)

  def updateList(self):
    names = []
    for device in DeviceList:
        names.append(device.nom)
    text_filter = filters.get(str(self.comboBox.currentText()))
    self.listWidget.clear()
    self.listWidget.insertItems(0, [text for text in names if text_filter in text + "All"])

  def getFilters(self):
    # Dictionnaire du filtre
    global filters
    filters = {"Dipole":"DP", "Quadripole":"QP", "Sextupole":"SP","Steerer":"STR", "All":"All"}
    #return les clefs du filtre
    return map(str,filters.keys())
	
  def readFileAlim(self):
    # Read Device name in file
	# Liste d'objets Alim
    global DeviceList
    DeviceList = []
    with open("alim_save.txt") as f:
        for line in f:
            #New Alim Objet
            DeviceList.append(Alim(line.strip()))
			
  def getDeviceAttributes(self):
    for device in DeviceList:
        device.readAttributes()
    self.updateTable()	

  def clearLayout(self,layout):
    print layout.count()
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())

class Alim:
  def __init__(self,name):
    self.nom = name
    self.labelDevice = QtGui.QLabel()
    self.labelDevice.setText(self.nom)
    self.afficheurCurrent = TaurusLabel()
    self.afficheurCurrent.setModel(self.nom+'/double_scalar')
    self.afficheurVoltage = TaurusLabel()
    self.afficheurVoltage.setModel(self.nom+'/float_scalar')
    self.commandButtonSwitch = TaurusCommandButton(command = 'SwitchStates', text = 'Switch State')
    self.commandButtonSwitch.setModel(self.nom)



myDialog = MyDialog()
myDialog.show()
sys.exit(app.exec_())


