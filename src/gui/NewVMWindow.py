#!/usr/bin/python
# -*- coding: utf-8 -*-


 ###########################################################################
 #   Copyright (C) 2011 by Olaf Radicke                                    #
 #                                                                         #
 #   This program is free software; you can redistribute it and/or modify  #
 #   it under the terms of the GNU General Public License as published by  #
 #   the Free Software Foundation; either version 3 of the License, or     #
 #   any later version.                                                    #
 #                                                                         #
 #   This program is distributed in the hope that it will be useful,       #
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
 #   GNU General Public License for more details.                          #
 #                                                                         #
 #   You should have received a copy of the GNU General Public License     #
 #   along with this program; if not, see                                  #
 #   http:#www.gnu.org/licenses/gpl.txt                                    #
 #                                                                         #
 ###########################################################################

import sys
import logging
import sqlite3
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from VMinfoDB import VMinfoDB 
from UserInfo import UserInfo


## @file NewVMWindow.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## This window is for create a new virtual machine.
class NewVMWindow(QtGui.QDialog):
  
    ## Database binding.
    __vmInfoDB = VMinfoDB()

    
    ## Home dir of user. Is a QLineEdit class.
    vmNameLineEdit = ""

    ## Combo box for select owener.
    owenerComboBox = ""
    
    ## Save information.
    #vmInfoDB = VMinfoDB()

    ## Constructor
    def __init__(self, vmInfoDB, parent=None): 
        logging.debug('init installMediaWindow....')
        
        self.__vmInfoDB = vmInfoDB
        QtGui.QDialog.__init__(self, parent)


        logging.debug('init installMediaWindow....')

        self.resize(500,280)
        self.setWindowTitle('Isar::New virtual machine')


        ## Main layout V
        vMainLayout = QtGui.QVBoxLayout()
        #centralWidget.setLayout(vMainLayout)
        self.setLayout(vMainLayout)
        

        # ----------- right box ---------------------------------

        # VBox right with GrouBox-frame
        editBox = QtGui.QGroupBox("Data of new machine")
        editBox.setMaximumWidth(600)
        vEditLayoutR = QtGui.QVBoxLayout()
        editBox.setLayout(vEditLayoutR)
        vMainLayout.addWidget(editBox)


        # Name
        hLayoutVMname = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hLayoutVMname)
        vmNameLabel = QtGui.QLabel("Name of machine:")
        hLayoutVMname.addWidget(vmNameLabel)
        self.vmNameLineEdit = QtGui.QLineEdit()
        hLayoutVMname.addWidget(self.vmNameLineEdit)

        # owner

        # Task stap typ
        hLayoutOwener = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hLayoutOwener)
        owenerLabel = QtGui.QLabel("Owener:")
        hLayoutOwener.addWidget(owenerLabel)
        self.owenerComboBox = QtGui.QComboBox()
        _allUser = self.__vmInfoDB.getAllUser()
        for _user in _allUser:
            self.owenerComboBox.addItem(_user.nickname)
        self.connect(self.owenerComboBox, QtCore.SIGNAL('currentIndexChanged(QString)'), QtCore.SLOT('owenerComboBoxChange(QString)'))
        hLayoutOwener.addWidget(self.owenerComboBox)

        
        # os


        # comment
        
        # ---------- Bottom area --------------------

        # Bottom layout H
        hBottomLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hBottomLayout)
        

        closePushButton = QtGui.QPushButton("Safe")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('newISOpathDialog()'))
        hBottomLayout.addWidget(closePushButton)

        closePushButton = QtGui.QPushButton("Cancel")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)



    ## Slot for safe edits
    @pyqtSlot()
    def safeEdits(self):       
        print "[safe edits...]"
        _name = ""
        for item in self.listview.selectedItems():
            print  ".." , item.text(0)
            _name = item.text(0)

        if str(_name) == "":
              infotext = "No user select!"
              QtGui.QMessageBox.information(self, "Error",str(infotext))
              return
        try:
            self.__vmInfoDB.updateISOpath(str(_name), str(self.vmNameLineEdit.text()))
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.information(self, "Error",str(infotext))
            return


    ## it is action if todoTypComboBox change
    @pyqtSlot(QtCore.QString)
    def owenerComboBoxChange(self, text):
        if (text == "bash_command"):
            self.originalFileLineEdit.setEnabled(False)
            self.replacementFileLineEdit.setEnabled(False)
            self.bashCommandLineEdit.setEnabled(True)
        elif(text == "replacement"):
            self.originalFileLineEdit.setEnabled(True)
            self.replacementFileLineEdit.setEnabled(True)
            self.bashCommandLineEdit.setEnabled(False)
        else:
            print "[OR2011_0320_2045]" 