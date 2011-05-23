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
import time
import subprocess

import GLOBALS
from DetailInfoDialog import DetailInfoDialog
from KVMManager import KVMManager
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from UserInfo import UserInfo
from VMinfoDB import VMinfoDB 
from VMinfo import VMinfo


## @file CloneVMWindow.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## This window is for cloneing a virtual machine.
class CloneVMWindow(QtGui.QDialog):
  
    ## Frame style
    __owneFramStyleSheet = GLOBALS.FRAM_STYLE_SHEET  

  
    ## Database binding.
    __vmInfoDB = VMinfoDB()

    ## Home dir of user. Is a QLineEdit class.
    vmNameLineEdit = ""

    ## Combo box for select owener.
    owenerComboBox = ""
    
    ## Box for comment.
    commentNameLabel  = "" 
    
    ## Name of original virtual machine
    __originalVM = ""
    
    ## Name of OS
    _distName = ""

    ## Constructor
    def __init__(self, vmInfoDB, parent=None): 
        logging.debug('init clone vm....')
        
        self.__vmInfoDB = vmInfoDB
        QtGui.QDialog.__init__(self, parent)


        logging.debug('init installMediaWindow....')

        self.resize(500,180)
        self.setWindowTitle('Isar::Clone a virtual machine')
        self.setStyleSheet(self.__owneFramStyleSheet)


        ## Main layout V
        vMainLayout = QtGui.QVBoxLayout()
        #centralWidget.setLayout(vMainLayout)
        self.setLayout(vMainLayout)
        

        # ----------- right box ---------------------------------

        # VBox right with GrouBox-frame
        editBox = QtGui.QGroupBox("Set data of Clone")
        editBox.setMaximumWidth(600)
        vEditLayoutR = QtGui.QVBoxLayout()
        editBox.setLayout(vEditLayoutR)
        vMainLayout.addWidget(editBox)


        # Name
        hLayoutVMname = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutVMname)
        vmNameLabel = QtGui.QLabel("Name of clone machine:")
        hLayoutVMname.addWidget(vmNameLabel)
        self.vmNameLineEdit = QtGui.QLineEdit()
        hLayoutVMname.addWidget(self.vmNameLineEdit)

        # owner

        # Selct owener
        hLayoutOwener = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutOwener)
        owenerLabel = QtGui.QLabel("Owener:")
        hLayoutOwener.addWidget(owenerLabel)
        self.owenerComboBox = QtGui.QComboBox()
        _allUser = self.__vmInfoDB.getAllUser()
        for _user in _allUser:
            self.owenerComboBox.addItem(_user.nickname)
        hLayoutOwener.addWidget(self.owenerComboBox)
        
        # life time
        hLayoutLifeTime = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutLifeTime)
        lifeTimeLabel = QtGui.QLabel("Life time:")
        hLayoutLifeTime.addWidget(lifeTimeLabel)
        self.lifeTimeSpinBox = QtGui.QSpinBox()
        self.lifeTimeSpinBox.setSuffix(" days")
        self.lifeTimeSpinBox.setRange(1, 10000) 
        self.lifeTimeSpinBox.setValue(60)
        hLayoutLifeTime.addWidget(self.lifeTimeSpinBox)
        
        # comment
        hLayoutVMcomment = QtGui.QVBoxLayout()
        vEditLayoutR.addLayout(hLayoutVMcomment)
        commentNameLabel = QtGui.QLabel("Comment:")
        hLayoutVMcomment.addWidget(commentNameLabel)
        self.commentNameLineEdit = QtGui.QLineEdit()
        hLayoutVMcomment.addWidget(self.commentNameLineEdit)
        
        
        # ---------- Bottom area --------------------

        # Bottom layout H
        hBottomLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hBottomLayout)
        

        closePushButton = QtGui.QPushButton("Clone now")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('cloneVM()'))
        hBottomLayout.addWidget(closePushButton)

        closePushButton = QtGui.QPushButton("Cancel")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)



    ## Slot for create new VM.
    @pyqtSlot()
    def cloneVM(self):
        print "[cloneVM...]"
        _result = ""
        _kvmManager = KVMManager()
        _vmInfo = VMinfo()
        
        _owner = str(self.owenerComboBox.currentText())
        _userInfo = self.__vmInfoDB.getUser(_owner)
        _lifeTime = str(self.lifeTimeSpinBox.value())
        _comment = unicode(self.commentNameLineEdit.text())
        
        _vmName = unicode(self.vmNameLineEdit.text())
        _vmName = _vmName.replace(unicode(" ", "utf-8"), "_")
        _vmName = _vmName.replace(unicode("ü", "utf-8"), "ue")
        _vmName = _vmName.replace(unicode("Ü", "utf-8"), "Ue")
        _vmName = _vmName.replace(unicode("ö", "utf-8"), "oe")
        _vmName = _vmName.replace(unicode("Ö", "utf-8"), "Oe")
        _vmName = _vmName.replace(unicode("ä", "utf-8"), "ae")
        _vmName = _vmName.replace(unicode("Ä", "utf-8"), "Ae")
        _vmName = _vmName.replace(unicode("ß", "utf-8"), "ss")
        self._distName = self._distName.replace(unicode(" ", "utf-8"), "_")
        _vmName = _owner + "_" + self._distName + "_" + _vmName
        
        _kvmManager.setOwnersHome(_userInfo.homedir)   
        _kvmManager.setMachineName(_vmName) 
        _kvmManager.setOriginalVM(self.__originalVM) 
        
        try:
            _result = _kvmManager.cloneMachine()

            mb = DetailInfoDialog()
            mb.setText("Result detail:")
            mb.setDetailedText(_result)
            mb.exec_()
            #QtGui.QMessageBox.information(self, "Result", _result) 
        except subprocess.CalledProcessError, e:
            infotext = "An error occurred:", (e.output.replace('\n',' ')).replace('\r',' ')
            QtGui.QMessageBox.critical(self, "Error",str(infotext))
            return  
        except OSError, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error",str(infotext))
            return  
            
        _vmInfo.name = _vmName
        _vmInfo.createdate = str(int(time.time()))
        _vmInfo.lifetimedays = _lifeTime
        _vmInfo.comment = _comment
        _vmInfo.mail = _userInfo.mail
        _vmInfo.image_file = _kvmManager.getImagePath()
        _vmInfo.owner = _userInfo.fullname + "(" + _userInfo.nickname + ")"
        _vmInfo.OS = self._distName
     
        try:
            self.__vmInfoDB.addVMinfo(_vmInfo)
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error",str(infotext))
            return  
        _infotext = "Ok, new virtual machine is created, \n \
                    and meta data is safed..."
        QtGui.QMessageBox.information(self, "OK",str(_infotext))
        self.close()

    ## it is action if owener Combo Box changes.
    @pyqtSlot(QtCore.QString)
    def owenerComboBoxChange(self, text):
        pass
 
    ## Set name of original virtual machine.
    def setOriginalVM(self, name):
        self.__originalVM = name
        
    ## Set Distribution of Clone.    
    def setDistName(self, name):
        self._distName = name