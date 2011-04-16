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
  
    ## Frame style
    __owneFramStyleSheet = GLOBALS.FRAM_STYLE_SHEET   
  
    ## Database binding.
    __vmInfoDB = VMinfoDB()

    ## Home dir of user. Is a QLineEdit class.
    vmNameLineEdit = ""

    ## Combo box for select owner.
    ownerComboBox = ""
    
    ## Combo box for select install ISO.
    isoComboBox  = ""   
    
    ## Spin box for RAM size.
    ramSpinBox  = ""   
    
    ## Spin box for hart disc size.
    hdSpinBox  = ""  
    
    ## Box for comment.
    commentNameLabel  = "" 
    


    ## Constructor
    # @param vmInfoDB a VMinfoDB class objekt.
    def __init__(self, vmInfoDB, parent=None): 
        logging.debug('init installMediaWindow....')
        
        self.__vmInfoDB = vmInfoDB
        QtGui.QDialog.__init__(self, parent)


        logging.debug('init installMediaWindow....')

        self.resize(500,180)
        self.setWindowTitle('Isar::New virtual machine')
        self.setStyleSheet(self.__owneFramStyleSheet)


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
        vEditLayoutR.addLayout(hLayoutVMname)
        vmNameLabel = QtGui.QLabel("Name of machine:")
        hLayoutVMname.addWidget(vmNameLabel)
        self.vmNameLineEdit = QtGui.QLineEdit()
        hLayoutVMname.addWidget(self.vmNameLineEdit)

        # owner

        # Selct owner
        hLayoutOwner = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutOwner)
        ownerLabel = QtGui.QLabel("Owner:")
        hLayoutOwner.addWidget(ownerLabel)
        self.ownerComboBox = QtGui.QComboBox()
        _allUser = self.__vmInfoDB.getAllUser()
        for _user in _allUser:
            self.ownerComboBox.addItem(_user.nickname)
        #self.connect(self.ownerComboBox, QtCore.SIGNAL('currentIndexChanged(QString)'), QtCore.SLOT('ownerComboBoxChange(QString)'))
        hLayoutOwner.addWidget(self.ownerComboBox)

        
        # Selkt ISO
        hLayoutISO = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutISO)
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
        vEditLayoutR.addLayout(hLayoutRAM)
        ramLabel = QtGui.QLabel("RAM:")
        hLayoutRAM.addWidget(ramLabel)
        self.ramSpinBox = QtGui.QSpinBox()
        self.ramSpinBox.setSuffix(" mb")
        self.ramSpinBox.setRange(256, 50000) 
        self.ramSpinBox.setValue(1000)
        hLayoutRAM.addWidget(self.ramSpinBox)
        
        # HD
        hLayoutHD = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutHD)
        hdLabel = QtGui.QLabel("Hard disc:")
        hLayoutHD.addWidget(hdLabel)
        self.hdSpinBox = QtGui.QSpinBox()
        self.hdSpinBox.setSuffix(" Gb")
        self.hdSpinBox.setRange(1, 1000) 
        self.hdSpinBox.setValue(10)
        hLayoutHD.addWidget(self.hdSpinBox)
        
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
        self.commentLineEdit = QtGui.QLineEdit()
        hLayoutVMcomment.addWidget(self.commentLineEdit)
        
        
        # ---------- Bottom area --------------------

        # Bottom layout H
        hBottomLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hBottomLayout)
        

        closePushButton = QtGui.QPushButton("Save")
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
        
        _owner = str(self.ownerComboBox.currentText())
        _userInfo = self.__vmInfoDB.getUser(_owner)
        _rawDistName = str(self.isoComboBox.currentText())
        _distName = _rawDistName.replace(" ", "_")
        _IsoPath = self.__vmInfoDB.getISOpath(_rawDistName)
        print "[_IsoPath]: ", _IsoPath
        if _IsoPath == -1:
            QtGui.QMessageBox.critical(self, "Error","No Paht of ISO found!")
            return
        _lifeTime = str(self.lifeTimeSpinBox.value() )
        _comment = unicode(self.commentLineEdit.text())
        
        _vmName = unicode(self.vmNameLineEdit.text())
        _vmName = _vmName.replace(unicode(" ", "utf-8"), "_")
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
            #QtGui.QMessageBox.critical(self, "Error",str(infotext))
            ret = QtGui.QMessageBox.critical(self, \
                                "Error", \
                                str(infotext), \
                                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ignore)

            if (ret == QtGui.QMessageBox.Cancel):   
                return  
        except OSError, e:
            infotext = "An error occurred:", e.args[0]
            #QtGui.QMessageBox.critical(self, "Error",str(infotext))
            ret = QtGui.QMessageBox.critical(self, \
                                "Error", \
                                str(infotext), \
                                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ignore)

            if (ret == QtGui.QMessageBox.Cancel):   
                return  
            
            
        _vmInfo.name = _vmName
        _vmInfo.createdate = str(int(time.time()))
        _vmInfo.lifetimedays = _lifeTime
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
                    and meta data is saved..."
        QtGui.QMessageBox.information(self, "OK",str(_infotext))
        self.close()

    ## it is action if owner Combo Box changes.
    @pyqtSlot(QtCore.QString)
    def ownerComboBoxChange(self, text):
        pass
 

    ## it is action if ISO Combo Box changes
    @pyqtSlot(QtCore.QString)
    def isoComboBoxChange(self, text):
        pass           