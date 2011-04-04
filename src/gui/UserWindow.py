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


## @file UserWindow.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## The window view info about users.
class UserWindow(QtGui.QDialog):
  
    ## Database binding.
    __vmInfoDB = VMinfoDB()

    ## User Infos of selected item
    __userInfo = UserInfo()

    ## Simple List
    listview = ""

    ## Full name of user. Is a QLineEdit class.
    fullnameLineEdit = ""
   
    ## Mail-Adress of user. Is a QLineEdit class.   
    mailLineEdit = ""
    
    ## Home dir of user. Is a QLineEdit class.
    userDirLineEdit = ""
    
    ## Save information.
    #vmInfoDB = VMinfoDB()

    ## Constructor
    def __init__(self, vmInfoDB, parent=None): 
        logging.debug('init UserWindow....')
        
        self.__vmInfoDB = vmInfoDB
        QtGui.QDialog.__init__(self, parent)


        logging.debug('init UserWindow....')

        self.resize(800,480)
        self.setWindowTitle('Isar::User')


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
        _haderList = ["nickname","email","realname","home"]
        self.listview.setColumnCount(len(_haderList))
        self.listview.setHeaderLabels(_haderList)
        vListLayoutL.addWidget(self.listview)
        self.connect(self.listview, QtCore.SIGNAL('itemSelectionChanged()'), QtCore.SLOT('fillDetailView()'))

        self.listview.addTopLevelItem( QtGui.QTreeWidgetItem(["OR","olaf@atix.de","Olaf Radicke","/home/or"]))

        # ----------- right box ---------------------------------

        # VBox right with GrouBox-frame
        editBox = QtGui.QGroupBox("Details")
        editBox.setMaximumWidth(600)
        vEditLayoutR = QtGui.QVBoxLayout()
        editBox.setLayout(vEditLayoutR)
        hMainLayout.addWidget(editBox)

	# Full name
        hFullnameLayout = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hFullnameLayout)
        
        nameLabel = QtGui.QLabel("Full Name:")
        hFullnameLayout.addWidget(nameLabel)
        self.fullnameLineEdit = QtGui.QLineEdit()
        hFullnameLayout.addWidget(self.fullnameLineEdit)        
        
	# Mail-address
        hMailLayout = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hMailLayout)
        
        mailLabel = QtGui.QLabel("Mail:")
        hMailLayout.addWidget(mailLabel)
        self.mailLineEdit = QtGui.QLineEdit()
        hMailLayout.addWidget(self.mailLineEdit) 
        
        # User dir
        hLayoutUserDir = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hLayoutUserDir)
        userDirLabel = QtGui.QLabel("User Dir:")
        hLayoutUserDir.addWidget(userDirLabel)
        self.userDirLineEdit = QtGui.QLineEdit()
        hLayoutUserDir.addWidget(self.userDirLineEdit)
        userDirPushButton = QtGui.QPushButton("...")
        self.connect(userDirPushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('selectUserDir()'))
        hLayoutUserDir.addWidget(userDirPushButton)        
        

	# comment
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
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('newUserDialog()'))
        hBottomLayout.addWidget(closePushButton)        
        
        closePushButton = QtGui.QPushButton("Delete")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('deleteUser()'))
        hBottomLayout.addWidget(closePushButton)

        closePushButton = QtGui.QPushButton("Close")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)
        
        self.refreshUserList()

    ## Slot delete user.
    @pyqtSlot()
    def deleteUser(self):
        print "[delete user...]"
        nickname = ""
        for item in self.listview.selectedItems():
            print  ".." , item.text(0)
            nickname = item.text(0)

        if str(nickname) == "":
              infotext = "No user select!"
              QtGui.QMessageBox.information(self, "Error",str(infotext))
              return
        else:
            try:
                self.__vmInfoDB.deleteUser(str(nickname))
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
        _nickname = ""
        for item in self.listview.selectedItems():
            print  ".." , item.text(0)
            _nickname = item.text(0)

        if str(_nickname) == "":
              infotext = "No user select!"
              QtGui.QMessageBox.information(self, "Error",str(infotext))
              return
        else:
            try:
                _userInfo = self.__vmInfoDB.getUser(str(_nickname))               
            except sqlite3.Error, e:
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.information(self, "Error",str(infotext))
                return
            if _userInfo == -1 or _userInfo == None:
                infotext = "Nickname not found!"
                QtGui.QMessageBox.information(self, "Error",str(infotext))
                return
            else:
                self.__userInfo = _userInfo    
                self.userDirLineEdit.setText( self.__userInfo.homedir )
                self.mailLineEdit.setText( self.__userInfo.mail )
                self.fullnameLineEdit.setText( self.__userInfo.fullname )
          
    ## A function with qt-slot. it's creade a new vm.
    @pyqtSlot()
    def newUserDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, "New User", "Nickname:", 0)
        if ok != True :
            logging.debug("[20110402201848] if: " + str(text) + str(ok))
            return
        else:
            logging.debug("[20110402201848] else: " + str(text) + str(ok))
            try:
                self.__vmInfoDB.addUser(str(text))
            except sqlite3.Error, e:
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.information(self, "Error",str(infotext))
                return

            self.__userInfo.nickname = str(text)
            self.refreshUserList()
      

        
    ## Refrash the list of tasks.
    @pyqtSlot()
    def refreshUserList(self):
        print "[refreshUserList]"
        userList = self.__vmInfoDB.getAllUser()
        self.listview.clear()
        for item in userList:
            qStringList = QtCore.QStringList([ \
                str(item.nickname),  \
                str(item.mail),  \
                str(item.fullname),  \
                str(item.homedir) \
            ])
            twItem = QtGui.QTreeWidgetItem(qStringList)
            self.listview.addTopLevelItem(twItem)


    ## Slot for safe edits
    @pyqtSlot()
    def safeEdits(self):       
        print "[safe edits...]"
        self.__userInfo.homedir =  str(self.userDirLineEdit.text())
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
    def selectUserDir(self):
        #print "selectUserDir()"
        dirname = QtGui.QFileDialog.getExistingDirectory(self, "Select home dir", self.userDirLineEdit.text(),QtGui.QFileDialog.ShowDirsOnly)
        self.userDirLineEdit.setText(dirname)

  