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
    vmNameLineEdit = ""

    ## Combo box for select owener.
    owenerComboBox = ""
    
    ## LineEdit widget for name of owner.
    __vmOwnerLineEdit = ""
    
    ## LineEdit widget for mail address of owner.
    mailLineEdit = ""
    
    ## LineEdit widget for image file of virtual machine
    vmImageLineEdit= ""
    
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
    # @param vmName name of a virtual machine.
    def __init__(self, vmInfoDB, vmName): 
        logging.debug('init installMediaWindow....')
        
        self.__vmInfoDB = vmInfoDB
        QtGui.QDialog.__init__(self, None)

        self.__vmData = self.__vmInfoDB.getVMinfo(vmName)
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
        editBox = QtGui.QGroupBox("Data of machine")
        editBox.setMaximumWidth(600)
        vEditLayoutR = QtGui.QVBoxLayout()
        editBox.setLayout(vEditLayoutR)
        vMainLayout.addWidget(editBox)


        # Name (ReadOnly)
        hLayoutVMname = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutVMname)
        vmNameLabel = QtGui.QLabel("Name of machine (read only):")
        hLayoutVMname.addWidget(vmNameLabel)
        self.vmNameLineEdit = QtGui.QLineEdit()
        self.vmNameLineEdit.setText(self.__vmData.name)
        self.vmNameLineEdit.setReadOnly(True)
        hLayoutVMname.addWidget(self.vmNameLineEdit)

        # owener 
        hLayoutOwner = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutOwner)
        owenerLabel = QtGui.QLabel("Owner:")
        hLayoutOwner.addWidget(owenerLabel)
        self.__vmOwnerLineEdit = QtGui.QLineEdit()
        self.__vmOwnerLineEdit.setText(self.__vmData.owner)
        hLayoutOwner.addWidget(self.__vmOwnerLineEdit)

        # life time
        hLayoutLifeTime = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutLifeTime)
        lifeTimeLabel = QtGui.QLabel("Life time:")
        hLayoutLifeTime.addWidget(lifeTimeLabel)
        self.lifeTimeSpinBox = QtGui.QSpinBox()
        self.lifeTimeSpinBox.setSuffix(" days")
        self.lifeTimeSpinBox.setRange(1, 10000) 
        print "[self.__vmData.lifetimedays] : ", self.__vmData.lifetimedays
        self.lifeTimeSpinBox.setValue(int(self.__vmData.lifetimedays))
        hLayoutLifeTime.addWidget(self.lifeTimeSpinBox)
        
        # comment
        hLayoutVMcomment = QtGui.QVBoxLayout()
        vEditLayoutR.addLayout(hLayoutVMcomment)
        commentNameLabel = QtGui.QLabel("Comment:")
        hLayoutVMcomment.addWidget(commentNameLabel)
        self.commentLineEdit = QtGui.QLineEdit()
        self.commentLineEdit.setText(self.__vmData.comment)
        hLayoutVMcomment.addWidget(self.commentLineEdit)
        
        # mail
        hLayoutVMmail = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutVMmail)
        mailLabel = QtGui.QLabel("Mail:")
        hLayoutVMmail.addWidget(mailLabel)
        self.mailLineEdit = QtGui.QLineEdit()
        self.mailLineEdit.setText(self.__vmData.mail)
        hLayoutVMmail.addWidget(self.mailLineEdit)
        
        # image_file (ReadOnly)
        hLayoutVMimageFile = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutVMimageFile)
        vmImageLabel = QtGui.QLabel("Image file (read only):")
        hLayoutVMimageFile.addWidget(vmImageLabel)
        self.vmImageLineEdit = QtGui.QLineEdit()
        self.vmImageLineEdit.setText(self.__vmData.image_file)
        self.vmImageLineEdit.setReadOnly(True)
        hLayoutVMimageFile.addWidget(self.vmImageLineEdit)  
        
        
        # ---------- Bottom area --------------------

        # Bottom layout H
        hBottomLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hBottomLayout)
        

        closePushButton = QtGui.QPushButton("Save")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('reConfigureVM()'))
        hBottomLayout.addWidget(closePushButton)

        closePushButton = QtGui.QPushButton("Cancel")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)



    ## Slot for create new VM.
    @pyqtSlot()
    def reConfigureVM(self):       
        print "[reConfigureVM...]"
        _result = ""
        _vmInfo = VMinfo()
        
        _owner = str(self.owenerComboBox.currentText())
        _userInfo = self.__vmInfoDB.getUser(_owner)
        _lifeTime = str(self.lifeTimeSpinBox.value())
        _comment = unicode(self.commentLineEdit.text())
        
        _vmName = unicode(self.vmNameLineEdit.text())
             
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

    ## it is action if owener Combo Box changes.
    @pyqtSlot(QtCore.QString)
    def owenerComboBoxChange(self, text):
        pass
 

    ## it is action if ISO Combo Box changes
    @pyqtSlot(QtCore.QString)
    def isoComboBoxChange(self, text):
        pass           