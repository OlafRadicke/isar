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


## @file installMediaWindow.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## The window view info about users.
class InstallMediaWindow(QtGui.QDialog):
  
    ## Database binding.
    __vmInfoDB = VMinfoDB()

    ## Simple List
    listview = ""
    
    __isoPathName = ""
    
    ## Home dir of user. Is a QLineEdit class.
    isoPathLineEdit = ""
    
    ## Save information.
    #vmInfoDB = VMinfoDB()

    ## Constructor
    def __init__(self, vmInfoDB, parent=None): 
        logging.debug('init installMediaWindow....')
        
        self.__vmInfoDB = vmInfoDB
        QtGui.QDialog.__init__(self, parent)


        logging.debug('init installMediaWindow....')

        self.resize(800,480)
        self.setWindowTitle('Isar::Instalations medias')


        ## Main layout V
        vMainLayout = QtGui.QVBoxLayout()
        #centralWidget.setLayout(vMainLayout)
        self.setLayout(vMainLayout)
        
        ## Main layout H
        hMainLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hMainLayout)


        # ----------- Left box ---------------------------------

        # VBox left with GrouBox-frame
        listBox = QtGui.QGroupBox("VM list")
        listBox.setMaximumWidth(600)
        vListLayoutL = QtGui.QVBoxLayout()
        listBox.setLayout(vListLayoutL)
        hMainLayout.addWidget(listBox)
        

        # -------------- List --------------

        self.listview = QtGui.QTreeWidget()
        _haderList = ["installations ISOs"]
        self.listview.setColumnCount(len(_haderList))
        self.listview.setHeaderLabels(_haderList)
        vListLayoutL.addWidget(self.listview)
        self.connect(self.listview, QtCore.SIGNAL('itemSelectionChanged()'), QtCore.SLOT('fillDetailView()'))

        # ----------- right box ---------------------------------

        # VBox right with GrouBox-frame
        editBox = QtGui.QGroupBox("Details")
        editBox.setMaximumWidth(600)
        vEditLayoutR = QtGui.QVBoxLayout()
        editBox.setLayout(vEditLayoutR)
        hMainLayout.addWidget(editBox)


        # ISO path
        hLayoutUserDir = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutUserDir)
        userDirLabel = QtGui.QLabel("Path of install ISO:")
        hLayoutUserDir.addWidget(userDirLabel)
        self.isoPathLineEdit = QtGui.QLineEdit()
        hLayoutUserDir.addWidget(self.isoPathLineEdit)
        userDirPushButton = QtGui.QPushButton("...")
        self.connect(userDirPushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('selectISOpath()'))
        hLayoutUserDir.addWidget(userDirPushButton)        
        

        # Safe buttom
        hSefeLayout = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hSefeLayout)
        
        safeButton = QtGui.QPushButton("Safe Edits")
        self.connect(safeButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('safeEdits()'))
        hSefeLayout.addWidget(safeButton) 
        
        
        vEditLayoutR.insertStretch(10000, 0)
        
        # ---------- Bottom area --------------------

        # Bottom layout H
        hBottomLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hBottomLayout)
        

        closePushButton = QtGui.QPushButton("New")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('newISOpathDialog()'))
        hBottomLayout.addWidget(closePushButton)        
        
        closePushButton = QtGui.QPushButton("Delete")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('deleteISOpath()'))
        hBottomLayout.addWidget(closePushButton)

        closePushButton = QtGui.QPushButton("Close")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)
        
        self.refreshUserList()

    ## Slot delete user.
    @pyqtSlot()
    def deleteISOpath(self):
        print "[delete ISO path...]"
        _name = ""
        for item in self.listview.selectedItems():
            print  ".." , item.text(0)
            _name = item.text(0)

        if str(_name) == "":
              infotext = "No user select!"
              QtGui.QMessageBox.information(self, "Error",str(infotext))
              return
        else:
            try:
                self.__vmInfoDB.deleteISOpath(str(_name))
            except sqlite3.Error, e:
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.information(self, "Error",str(infotext))
                return

            self.refreshUserList()
          
    ## Slot delete user.
    @pyqtSlot()
    def fillDetailView(self):
        print "[fillDetailView...]"
        _userInfo = ""
        _name = ""
        for item in self.listview.selectedItems():
            print  ".." , item.text(0)
            _name = item.text(0)

        if str(_name) == "":
              infotext = "No user select!"
              QtGui.QMessageBox.information(self, "Error",str(infotext))
              return
        else:
            try:
                _path = self.__vmInfoDB.getISOpath(str(_name))               
            except sqlite3.Error, e:
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.information(self, "Error",str(infotext))
                return
            if _userInfo == -1 or _userInfo == None:
                infotext = "ISO name not found!"
                QtGui.QMessageBox.information(self, "Error",str(infotext))
                return
            else:
                self.isoPathLineEdit.setText( _path )
          
    ## A function with qt-slot. it's creade a new vm.
    @pyqtSlot()
    def newISOpathDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, "New ISO path", "Label name (not path):", 0)
        if ok != True :
            logging.debug("[201104] if: " + str(text) + str(ok))
            return
        else:
            logging.debug("[201104] else: " + str(text) + str(ok))
            try:
                self.__vmInfoDB.addISOpath(str(text))
            except sqlite3.Error, e:
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.information(self, "Error",str(infotext))
                return

            self.__isoPathName = str(text)
            self.refreshUserList()
      

        
    ## Refrash the list of tasks.
    @pyqtSlot()
    def refreshUserList(self):
        print "[refreshUserList]"
        nameList = self.__vmInfoDB.getAllISOnames()
        self.listview.clear()
        for item in nameList:
            qStringList = QtCore.QStringList( [ str(item) ] )
            twItem = QtGui.QTreeWidgetItem(qStringList)
            self.listview.addTopLevelItem(twItem)


    ## Slot for safe edits
    @pyqtSlot()
    def safeEdits(self):       
        print "[safe edits...]"
        self.__userInfo.homedir =  str(self.isoPathLineEdit.text())
        self.__userInfo.mail =  str(self.mailLineEdit.text())
        self.__userInfo.fullname =  str(self.fullnameLineEdit.text())
        try:
            self.__vmInfoDB.updateUser(self.__userInfo)
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.information(self, "Error",str(infotext))
            return

    ## Slot with file dialog, for selct a dir.
    @pyqtSlot()
    def selectISOpath(self):
        #print "selectISOpath()"
        dirname = QtGui.QFileDialog.getOpenFileName(self, "Select ISO image", self.isoPathLineEdit.text(),".iso .ISO")
        self.isoPathLineEdit.setText(dirname)

  