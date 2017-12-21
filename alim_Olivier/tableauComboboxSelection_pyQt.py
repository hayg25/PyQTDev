#!/usr/bin/env python
# -*- coding: utf-8 *-

import sys
import os
import taurus

from taurus.qt.qtgui.button import TaurusCommandButton

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import *

app = QtGui.QApplication(sys.argv)

class MyDialog(QtGui.QWidget):


  def __init__(self):
    QtGui.QWidget.__init__(self)
    uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tableauComboboxSelection_pyQt_layout.ui"), self)
    self.readFileAlim()
    self.comboBox.currentIndexChanged.connect(self.updateList)
    self.comboBox.currentIndexChanged.connect(self.updateTable)
    self.comboBox.clear()
    self.comboBox.insertItems(0, self.getFilters())
    self.updateList()
    self.updateTable()
    # Timer 
    self.timer = QtCore.QTimer(self)
    self.connect(self.timer, QtCore.SIGNAL("timeout()"),self.getDeviceAttributes)
    self.timer.start(1000)

  def updateTable(self):
    # filtre venant du choix du combobox
	# Recherche dans le dictionnaire
    text_filter = filters.get(str(self.comboBox.currentText()))
    # nettoyage de la zone a ecrire
    self.tableWidget.clear()
	# Header du tableau a ecrire après chaque .clear
    self.tableWidget.setHorizontalHeaderLabels(['Names','Current','Voltage'])
    # If "All" is used, no filter is applied
    # cette methode n'existe pas : il faut trouver un equivalent
    # self.tableWidget.insertItems(0,[text for text in items if text_filter in text + "All"])
    k=-1
    for device in DeviceList:
        if text_filter in device.nom+"All":
            k+=1
			# redimensionnement du tableau
            self.tableWidget.setRowCount(k+1)
			# ecriture dans le tableau
            self.tableWidget.setItem(k,0,QtGui.QTableWidgetItem(device.nom))
            self.tableWidget.setItem(k,1,QtGui.QTableWidgetItem(str(device.current)))
            self.tableWidget.setItem(k,2,QtGui.QTableWidgetItem(str(device.voltage)))
            #self.tableWidget.setItem(k,3,device.commandButtonSwitch)

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

class Alim:
  def __init__(self,name):
    self.nom = name
    self.current = 0.4
    self.voltage = 5.0
    self.currentSetpointPM = 0.0
    self.status = ""
    self.state = ""	
    #self.commandButtonSwitch = TaurusCommandButton(command = 'SwitchStates', text = 'Switch State')
    #self.commandButtonSwitch.setModel(self.nom)
	
  def readAttributes(self):
    device = taurus.Device(self.nom)
    #self.current = device.getAttribute('Current')
    self.current = round(device.read_attribute("double_scalar").value,2)
    #self.voltage = device.getAttribute('Voltage')
    self.voltage = round(device.read_attribute("float_scalar").value,2)



myDialog = MyDialog()
myDialog.show()
sys.exit(app.exec_())


