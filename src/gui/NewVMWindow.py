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
from KVMManager import KVMManager


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
    
    ## Combo box for select install ISO.
    isoComboBox  = ""   
    
    ## Spin box for RAM size.
    ramSpinBox  = ""   
    
    ## Spin box for hart disc size.
    hdSpinBox  = ""  
    
    ## Box for comment.
    commentNameLabel  = "" 
    


    ## Constructor
    def __init__(self, vmInfoDB, parent=None): 
        logging.debug('init installMediaWindow....')
        
        self.__vmInfoDB = vmInfoDB
        QtGui.QDialog.__init__(self, parent)


        logging.debug('init installMediaWindow....')

        self.resize(500,180)
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

        # Selct owener
        hLayoutOwener = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hLayoutOwener)
        owenerLabel = QtGui.QLabel("Owener:")
        hLayoutOwener.addWidget(owenerLabel)
        self.owenerComboBox = QtGui.QComboBox()
        _allUser = self.__vmInfoDB.getAllUser()
        for _user in _allUser:
            self.owenerComboBox.addItem(_user.nickname)
        #self.connect(self.owenerComboBox, QtCore.SIGNAL('currentIndexChanged(QString)'), QtCore.SLOT('owenerComboBoxChange(QString)'))
        hLayoutOwener.addWidget(self.owenerComboBox)

        
        # Selkt ISO
        hLayoutISO = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hLayoutISO)
        isoLabel = QtGui.QLabel("Install ISO:")
        hLayoutISO.addWidget(isoLabel)
        self.isoComboBox = QtGui.QComboBox()
        _allISOs = self.__vmInfoDB.getAllISOnames()
        for _isoName in _allISOs:
            self.isoComboBox.addItem(_isoName)
        #self.connect(self.isoComboBox, QtCore.SIGNAL('currentIndexChanged(QString)'), QtCore.SLOT('isoComboBoxChange(QString)'))
        hLayoutISO.addWidget(self.isoComboBox)
        
        # RAM
        hLayoutRAM = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hLayoutRAM)
        ramLabel = QtGui.QLabel("RAM:")
        hLayoutRAM.addWidget(ramLabel)
        self.ramSpinBox = QtGui.QSpinBox()
        self.ramSpinBox.setSuffix(" mb")
        self.ramSpinBox.setRange(256, 50000) 
        self.ramSpinBox.setValue(1000)
        hLayoutRAM.addWidget(self.ramSpinBox)
        
        # HD
        hLayoutHD = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hLayoutHD)
        hdLabel = QtGui.QLabel("Hart disc:")
        hLayoutHD.addWidget(hdLabel)
        self.hdSpinBox = QtGui.QSpinBox()
        self.hdSpinBox.setSuffix(" Gb")
        self.hdSpinBox.setRange(1, 1000) 
        self.hdSpinBox.setValue(10)
        hLayoutHD.addWidget(self.hdSpinBox)
        
        # comment
        hLayoutVMcomment = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hLayoutVMcomment)
        commentNameLabel = QtGui.QLabel("Comment:")
        hLayoutVMcomment.addWidget(commentNameLabel)
        self.commentNameLineEdit = QtGui.QLineEdit()
        hLayoutVMcomment.addWidget(self.commentNameLineEdit)
        
        
        # ---------- Bottom area --------------------

        # Bottom layout H
        hBottomLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hBottomLayout)
        

        closePushButton = QtGui.QPushButton("Safe")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('createNewVM()'))
        hBottomLayout.addWidget(closePushButton)

        closePushButton = QtGui.QPushButton("Cancel")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)



    ## Slot for create new VM.
    @pyqtSlot()
    def createNewVM(self):       
        print "[createNewVM...]"
        _kvmManager = KVMManager()
        
        _owner = str(self.owenerComboBox.currentText())
        _userInfo = self.__vmInfoDB.getUser(_owner)
        _distName = str(self.isoComboBox.currentText())
        _IsoPath = self.__vmInfoDB.getISOpath(_distName)
        
        _kvmManager.setOwner(_owner)
        _kvmManager.setOwnersHome(_userInfo.homedir)   
        _kvmManager.setMachineName(str(self.vmNameLineEdit.text())) 
        _kvmManager.setDistribution(_distName)
        _kvmManager.setRAM(str(self.ramSpinBox.value()))
        _kvmManager.setHdSize(str(self.hdSpinBox.value()))
        _kvmManager.setIsoPath(_IsoPath)
        
        _result = _kvmManager.createNewMachine()
        
        try:
            QtGui.QMessageBox.information(self, "Result", _result)
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error",str(infotext))
            return            

    ## it is action if owener Combo Box changes.
    @pyqtSlot(QtCore.QString)
    def owenerComboBoxChange(self, text):
        pass
 

    ## it is action if ISO Combo Box changes
    @pyqtSlot(QtCore.QString)
    def isoComboBoxChange(self, text):
        pass           