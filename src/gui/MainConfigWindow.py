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
import GLOBALS
#import time
#import subprocess
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from VMinfoDB import VMinfoDB 
from UserInfo import UserInfo
from VMinfo import VMinfo


## @file MainConfigWindow.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## This window is for configure the aplication.
class MainConfigWindow(QtGui.QDialog):
  
    ## Frame style
    __owneFramStyleSheet = GLOBALS.FRAM_STYLE_SHEET

    ## Database binding.
    __vmInfoDB = VMinfoDB()
    

    ## Address from KVM-Server. Is a QLineEdit class.
    __sshAddressLineEdit = ""
    
    ## Rame of ssh user.
    __sshUserLineEdit = ""
    
    ## Typ: CheckBox.  Using ssh, if checked.
    __useSshCheckBox = ""

    ## Constructor
    # @param vmInfoDB a VMinfoDB class objekt.
    def __init__(self, vmInfoDB): 
        logging.debug('init MainConfigWindow....')
        
        self.__vmInfoDB = vmInfoDB
        QtGui.QDialog.__init__(self, None)


        self.resize(500,180)
        self.setWindowTitle('Isar::Config')
        self.setStyleSheet(self.__owneFramStyleSheet)


        ## Main layout V
        vMainLayout = QtGui.QVBoxLayout()
        #centralWidget.setLayout(vMainLayout)
        self.setLayout(vMainLayout)
        

        # ----------- right box ---------------------------------

        # VBox right with GrouBox-frame
        sshBox = QtGui.QGroupBox("ssh config")
        sshBox.setMaximumWidth(600)
        vSshLayout = QtGui.QVBoxLayout()
        sshBox.setLayout(vSshLayout)
        vMainLayout.addWidget(sshBox)


        # Stop before execute task
        self.__useSshCheckBox = QtGui.QCheckBox("use ssh")
        vSshLayout.addWidget(self.__useSshCheckBox)

        # Name (ReadOnly)
        hLayoutSshAddress = QtGui.QHBoxLayout()
        vSshLayout.addLayout(hLayoutSshAddress)
        sshAddressLabel = QtGui.QLabel("Address:")
        hLayoutSshAddress.addWidget(sshAddressLabel)
        self.__sshAddressLineEdit = QtGui.QLineEdit()
        #self.__sshAddressLineEdit.setText("")
        hLayoutSshAddress.addWidget(self.__sshAddressLineEdit)

        # owener 
        hLayoutSshUser = QtGui.QHBoxLayout()
        vSshLayout.addLayout(hLayoutSshUser)
        sshUserLabel = QtGui.QLabel("ssh user:")
        hLayoutSshUser.addWidget(sshUserLabel)
        self.__sshUserLineEdit = QtGui.QLineEdit()
        #self.__sshUserLineEdit.setText("")
        hLayoutSshUser.addWidget(self.__sshUserLineEdit)


        
        # ---------- Bottom area --------------------

        # Bottom layout H
        hBottomLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hBottomLayout)
        

        closePushButton = QtGui.QPushButton("Save")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('saveConfig()'))
        hBottomLayout.addWidget(closePushButton)

        closePushButton = QtGui.QPushButton("Cancel")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)

        self.fillData()

    ## Read date from data base and set in form.
    def fillData(self):
        print "[fillData]"
        _isSsh = ""
        _sshAddress = ""
        _sshUser = ""
        
        try:
            _isSsh = self.__vmInfoDB.getConfiValue("ssh_conact")
            _sshAddress = self.__vmInfoDB.getConfiValue("ssh_address")
            _sshUser = self.__vmInfoDB.getConfiValue("ssh_user")
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error",str(infotext))

        if _isSsh == "True":
            self.__useSshCheckBox.setCheckState(QtCore.Qt.Checked)
        else:
            self.__useSshCheckBox.setCheckState(QtCore.Qt.Unchecked)
        self.__sshAddressLineEdit.setText(_sshAddress)
        self.__sshUserLineEdit.setText(_sshUser)
        return

    ## Slot for safe config.
    @pyqtSlot()
    def saveConfig(self):       
        print "[saveConfig...]"
        if self.__useSshCheckBox.checkState():
            _isSsh = "True"
        else:
            _isSsh = "False"
        _sshAddress = str(self.__sshAddressLineEdit.text())
        _sshUser = str(self.__sshUserLineEdit.text())

        try:
            self.__vmInfoDB.setConfiValue("ssh_conact", _isSsh)
            self.__vmInfoDB.setConfiValue("ssh_address", _sshAddress)
            self.__vmInfoDB.setConfiValue("ssh_user", _sshUser)
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error",str(infotext))
            return  
        _infotext = "Ok, savted changes..."
        QtGui.QMessageBox.information(self, "OK",str(_infotext))
        self.close()

         