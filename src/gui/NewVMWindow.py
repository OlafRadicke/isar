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
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from VMinfoDB import VMinfoDB 
from UserInfo import UserInfo
from KVMManager import KVMManager
from VMinfo import VMinfo


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
        
        # life time
        hLayoutLifeTime = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hLayoutLifeTime)
        lifeTimeLabel = QtGui.QLabel("Life time:")
        hLayoutLifeTime.addWidget(lifeTimeLabel)
        self.lifeTimeSpinBox = QtGui.QSpinBox()
        self.lifeTimeSpinBox.setSuffix(" days")
        self.lifeTimeSpinBox.setRange(1, 10000) 
        self.lifeTimeSpinBox.setValue(60)
        hLayoutLifeTime.addWidget(self.lifeTimeSpinBox)
        
        # comment
        hLayoutVMcomment = QtGui.QVBoxLayout()
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
        _result = ""
        _kvmManager = KVMManager()
        _vmInfo = VMinfo()
        
        _owner = str(self.owenerComboBox.currentText())
        _userInfo = self.__vmInfoDB.getUser(_owner)
        _rawDistName = str(self.isoComboBox.currentText())
        _distName = _rawDistName.replace(" ", "_")
        _IsoPath = self.__vmInfoDB.getISOpath(_rawDistName)
        print "[_IsoPath]: ", _IsoPath
        if _IsoPath == -1:
            QtGui.QMessageBox.critical(self, "Error","No Paht of ISO found!")
            return
        _lifeTime = str(self.lifeTimeSpinBox)
        _comment = unicode(self.commentNameLineEdit.text)
        
        _vmName = unicode(self.vmNameLineEdit.text())
        _vmName = _vmName.replace(unicode("ü", "utf-8"), "ue")
        _vmName = _vmName.replace(unicode("Ü", "utf-8"), "Ue")
        _vmName = _vmName.replace(unicode("ö", "utf-8"), "oe")
        _vmName = _vmName.replace(unicode("Ö", "utf-8"), "Oe")
        _vmName = _vmName.replace(unicode("ä", "utf-8"), "ae")
        _vmName = _vmName.replace(unicode("Ä", "utf-8"), "Ae")
        _vmName = _vmName.replace(unicode("ß", "utf-8"), "ss")
        _vmName = _owner + "_" + _distName + "_" + _vmName
        
        _kvmManager.setOwnersHome(_userInfo.homedir)   
        _kvmManager.setMachineName(_vmName) 
        _kvmManager.setRAM(str(self.ramSpinBox.value()))
        _kvmManager.setHdSize(str(self.hdSpinBox.value()))
        _kvmManager.setIsoPath(_IsoPath)
        
        try:  
            _result = _kvmManager.createNewMachine()
            QtGui.QMessageBox.information(self, "Result", _result) 
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
        _vmInfo.livetimedays = _lifeTime
        _vmInfo.comment = _comment
        _vmInfo.mail = _userInfo.mail
        _vmInfo.image_file = _kvmManager.getImagePath()
        _vmInfo.owner = _userInfo.fullname + "(" + _userInfo.nickname + ")"
        _vmInfo.OS = _rawDistName
     
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
 

    ## it is action if ISO Combo Box changes
    @pyqtSlot(QtCore.QString)
    def isoComboBoxChange(self, text):
        pass           