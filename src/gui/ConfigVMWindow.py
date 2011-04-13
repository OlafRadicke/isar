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
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from VMinfoDB import VMinfoDB 
from UserInfo import UserInfo
from VMinfo import VMinfo


## @file ConfigVMWindow.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## This window is for configure data of a exist virtual machine.
class ConfigVMWindow(QtGui.QDialog):
  
    ## Frame style
    __owneFramStyleSheet = GLOBALS.FRAM_STYLE_SHEET

    ## Database binding.
    __vmInfoDB = VMinfoDB()
    
    ## Infos about a virtual machine as VMinfo object.
    __vmData = ""

    ## Home dir of user. Is a QLineEdit class.
    __sshAddressLineEdit = ""
    
    ## LineEdit widget for name of owner.
    __sshUserLineEdit = ""
    
    ## Typ: CheckBox.  Is stoped before execute task, if "True"
    __useSshCheckBox = ""

    ## Constructor
    # @param vmInfoDB a VMinfoDB class objekt.
    # @param vmName name of a virtual machine.
    def __init__(self, vmInfoDB, vmName): 
        logging.debug('init ConfigVMWindow....')
        
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
        vListLayoutR3.addWidget(self.__useSshCheckBox)

        # Name (ReadOnly)
        hLayoutSshAddress = QtGui.QHBoxLayout()
        vSshLayout.addLayout(hLayoutSshAddress)
        sshAddressLabel = QtGui.QLabel("Address:")
        hLayoutSshAddress.addWidget(sshAddressLabel)
        self.__sshAddressLineEdit = QtGui.QLineEdit()
        self.__sshAddressLineEdit.setText(self.__vmData.name)
        self.__sshAddressLineEdit.setReadOnly(True)
        hLayoutSshAddress.addWidget(self.__sshAddressLineEdit)

        # owener 
        hLayoutSshUser = QtGui.QHBoxLayout()
        vSshLayout.addLayout(hLayoutSshUser)
        sshUserLabel = QtGui.QLabel("ssh user:")
        hLayoutSshUser.addWidget(sshUserLabel)
        self.__sshUserLineEdit = QtGui.QLineEdit()
        self.__sshUserLineEdit.setText(self.__vmData.owner)
        hLayoutSshUser.addWidget(self.__sshUserLineEdit)


        
        # ---------- Bottom area --------------------

        # Bottom layout H
        hBottomLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hBottomLayout)
        

        closePushButton = QtGui.QPushButton("Safe")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('safeConfig()'))
        hBottomLayout.addWidget(closePushButton)

        closePushButton = QtGui.QPushButton("Cancel")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)



    ## Slot for safe config.
    @pyqtSlot()
    def safeConfig(self):       
        print "[safeConfig...]"
        
        return
        
        _result = ""
        _vmInfo = VMinfo()
        
        _owner = str(self.owenerComboBox.currentText())
        _userInfo = self.__vmInfoDB.getUser(_owner)
        _lifeTime = str(self.lifeTimeSpinBox.value())
        _comment = unicode(self.commentLineEdit.text())
        
        _vmName = unicode(self.__sshAddressLineEdit.text())
             
        _vmInfo.name = _vmName
        _vmInfo.lifetimedays = _lifeTime
        _vmInfo.comment = _comment
        _vmInfo.mail = _userInfo.mail
        _vmInfo.owner = _userInfo.fullname + "(" + _userInfo.nickname + ")"
     
        try:     
            self.__vmInfoDB.updateVMinfo(_vmInfo)
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error",str(infotext))
            return  
        _infotext = "Ok, safted changes..."
        QtGui.QMessageBox.information(self, "OK",str(_infotext))
        self.close()

         