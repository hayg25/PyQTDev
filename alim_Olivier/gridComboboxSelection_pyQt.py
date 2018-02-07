#!/usr/bin/env python
# -*- coding: utf-8 *-

import sys
import os
import taurus

from taurus.qt.qtgui.button import TaurusCommandButton
from taurus.qt.qtgui.display import TaurusLabel
from taurus.qt.qtgui.input import TaurusWheelEdit

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import *

app = QtGui.QApplication(sys.argv)

class MyDialog(QtGui.QWidget):


    def __init__(self):
        QtGui.QWidget.__init__(self)
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gridComboboxSelection_pyQt_layout.ui"), self)
        self.contenu = QtGui.QWidget()
        self.gridLayout = QtGui.QGridLayout()
        # Taille des collonnes
        self.gridLayout.setColumnMinimumWidth(0, 100)
        self.gridLayout.setColumnMinimumWidth(1, 70)
        self.gridLayout.setColumnMinimumWidth(2, 70)
        self.gridLayout.setColumnMinimumWidth(3, 70)
        # self.gridLayout.setColumnMinimumWidth(4, 60)
        self.gridLayout.setColumnMinimumWidth(5, 60)
        # self.gridLayout.setColumnMinimumWidth(6, 80)
        self.gridLayout.setColumnMinimumWidth(7, 80)
        self.contenu.setLayout(self.gridLayout)
        self.readFileAlim()
        self.getFilterZones()
        self.comboBoxType.currentIndexChanged.connect(self.updateTable)
        self.comboBoxType.clear()
        self.comboBoxType.insertItems(0, self.getFilterTypes())
        self.comboBoxZone.currentIndexChanged.connect(self.updateTable)
        self.comboBoxZone.clear()
        self.comboBoxZone.insertItems(0, self.getFilterZones())
        self.selectButton.clicked.connect(self.selectAll)
        self.startButton.clicked.connect(self.startAll)
        self.stopButton.clicked.connect(self.stopAll)
        # self.updateList()
        # self.updateTable()

    def updateTable(self):
        global checkList
        checkList = []
        # filtre venant du choix du combobox
        # Recherche dans le dictionnaire
        if filterTypes.has_key(str(self.comboBoxType.currentText())):
            value_filterTypes = filterTypes.get(str(self.comboBoxType.currentText()))
        else:
            value_filterTypes = 'All'

        if filterZones.has_key(str(self.comboBoxZone.currentText())):
            value_filterZones = filterZones.get(str(self.comboBoxZone.currentText()))
        else:
            value_filterZones = 'All'

        # nettoyage de la zone a ecrire
        self.clearLayout(self.gridLayout)
        # Header du tableau a ecrire après chaque .clear
        #self.tableWidget.setHorizontalHeaderLabels(['Names','Current','Voltage'])
        # If "All" is used, no filter is applied
        # cette methode n'existe pas : il faut trouver un equivalent
        # self.tableWidget.insertItems(0,[text for text in items if text_filter in text + "All"])
        k=-1
        #self.gridLayout.addWidget(self.styledPanel(),k,0,1,8)
        for device in DeviceList:
            if value_filterTypes in device+"All":
                if value_filterZones in device+"All":
                    # test line
                    k += 1
                    self.gridLayout.addWidget(self.Hline(), k, 0, 1, 8)
                    k += 1
                    self.gridLayout.setRowMinimumHeight(k, 40)
                    # Bouton ouverture device
                    self.buttonDevice = QtGui.QPushButton()
                    self.buttonDevice.setText(device)
                    self.buttonDevice.clicked.connect(AfficheDevice(device))
                    self.gridLayout.addWidget(self.buttonDevice, k, 0)
                    # Afficheur courant
                    self.afficheurCurrent = TaurusLabel()
                    self.afficheurCurrent.setModel(device + '/double_scalar')
                    self.gridLayout.addWidget(self.afficheurCurrent, k, 1)
                    # Afficheur tension
                    self.afficheurVoltage = TaurusLabel()
                    self.afficheurVoltage.setModel(device + '/float_scalar')
                    self.gridLayout.addWidget(self.afficheurVoltage, k, 2)
                    # Lecture consigne courant
                    self.afficheurCurrentSP = TaurusLabel()
                    self.afficheurCurrentSP.setModel(device + '/ampli')
                    self.gridLayout.addWidget(self.afficheurCurrentSP, k, 3)
                    # Ecriture consigne courant
                    self.writeCurrentSP = TaurusWheelEdit()
                    self.writeCurrentSP.setModel(device + '/ampli')
                    self.gridLayout.addWidget(self.writeCurrentSP, k, 4)
                    # Afficheur etat
                    self.afficheurState = TaurusLabel()
                    self.afficheurState.setModel(device + '/State')
                    self.gridLayout.addWidget(self.afficheurState, k, 5)
                    # CheckBox de selection
                    self.buttonSelect = QtGui.QCheckBox(device, self)
                    self.gridLayout.addWidget(self.buttonSelect, k, 6)
                    checkList.append(self.buttonSelect)
                    # Bouton commande Taurus
                    self.commandButtonSwitch = TaurusCommandButton(command = 'SwitchStates', text = 'Switch State')
                    self.commandButtonSwitch.setModel(device)
                    self.gridLayout.addWidget(self.commandButtonSwitch, k, 7)

        self.scrollArea.setWidget(self.contenu)

    def readFileAlim(self):
        # Read Device name in file
        # List of Device name
        global DeviceList
        DeviceList = []
        with open("alim.txt") as f:
            for line in f:
                DeviceList.append(line.strip())

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

    def getFilterTypes(self):
        # Dictionnaire du filtre
        global filterTypes
        filterTypes = {"Dipole":"DP", "Quadripole":"QP", "Sextupole":"SP","Steerer":"STR","Coil":"COL"}
        #return les clefs du filtre
        return map(str,filterTypes.keys()+['All'])

    def getFilterZones(self):
        # Dictionnaire du filtre
        global filterZones
        filterZones = {"Linac":"LI", "Transfert line":"TL", "Extraction line":"EL", "Ring C1":"RI-C1", "Ring-C2":"RI-C2"}
        #return les clefs du filtre
        return map(str,filterZones.keys()+['All'])

    def selectAll(self):
        for check in checkList:
            check.setCheckState(True)

    def startAll(self):
        for check in checkList:
            if check.checkState():
                print (check.text())

    def stopAll(self):
        for check in checkList:
            if check.checkState():
                print (check.text())

    def Hline(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def Vline(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def styledPanel(self):
        line = QFrame()
        line.setFrameShape(QFrame.StyledPanel)
        line.setFrameShadow(QFrame.Sunken)
        return line

class AfficheDevice:
    def __init__(self,name):
        self.name = name
    def __call__(self):
        print (self.name)

myDialog = MyDialog()
myDialog.show()
sys.exit(app.exec_())
