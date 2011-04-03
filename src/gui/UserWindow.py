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

        self.resize(800,680)
        self.setWindowTitle('Isar::User')



        # ----------- toolbar ---------------------
        #self.toolbar = self.addToolBar('tools')
        
        #toolNew = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New VM', self)
        #toolNew.setShortcut('Ctrl+N')
        #self.connect(toolNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('newVMDialog()'))
        #self.toolbar.addAction(toolNew)

        #toolRemove = QtGui.QAction(QtGui.QIcon('icons/remove.png'), 'Delete VM', self)
        #toolNew.setShortcut('Ctrl+X')
        #self.connect(toolRemove, QtCore.SIGNAL('triggered()'), QtCore.SLOT('deleteVM()'))
        #self.toolbar.addAction(toolRemove)

        # ----------- toolbar end ------------------------



        ## Main Widget
        #centralWidget = QtGui.QWidget()
        #self.setCentralWidget(centralWidget)

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
        self.connect(self.listview, QtCore.SIGNAL('itemSelectionChanged()'), QtCore.SLOT('fillTaskView()'))

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
        
	# ---------- Bottom area --------------------

        # Bottom layout H
        hBottomLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hBottomLayout)
        

        closePushButton = QtGui.QPushButton("New")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('newVMDialog()'))
        hBottomLayout.addWidget(closePushButton)        
        
        closePushButton = QtGui.QPushButton("Delete")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)

        closePushButton = QtGui.QPushButton("Close")
        self.connect(closePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        hBottomLayout.addWidget(closePushButton)


    ## A function with qt-slot. it's creade a new vm.
    @pyqtSlot()
    def newVMDialog(self):
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
	      QtGui.QMessageBox.information(self, "Error",infotext)
	      return
    
          self.__userInfo.nickname = text
          #taskTyp = TaskTyp()
          #taskTyp.ID = text
          #self.tasksSettings.addTaskTyp(taskTyp)
          self.refreshVMList()
      

        
    ## Refrash the list of tasks.
    @pyqtSlot()
    def refreshVMList(self):
        pass
        #self.tasksSettings.reLoad()
        #self.taskBox.setTasksSettings(self.tasksSettings)
        #self.listview.clear ()
        #count = 0
        #for item in self.tasksSettings.getStoryboard():
            #print "[debug] ", item
            #self.listview.insertItem(count, item)
            #count = count + 1


    ## A function with qt-slot. it's fill the TaskView with data. 
    @pyqtSlot()
    def fillTaskView(self):
        pass
        #todo = ""
        #for item in self.listview.selectedItems():
            #print  "[debug] .." , item.text()
            #todo = item.text()

        #if( todo == "" ):
            #self.statusBar().showMessage('No ToDo select...')
        #else:
          #taskTyp = self.tasksSettings.getTaskTyp(todo)
          #self.taskBox.setTaskTyp(taskTyp)


    ## Function delete a task
    @pyqtSlot()
    def deleteVM(self):
        logging.debug("[20110402201311] deleteVM")
        #todo = ""
        #for item in self.listview.selectedItems():
            #print  ".." , item.text()
            #todo = item.text()

        #if( todo == "" ):
            #self.statusBar().showMessage('No ToDo select...')
        #else:
          #taskTyp = self.tasksSettings.getTaskTyp(todo)
          #self.tasksSettings.deleteTask(taskTyp)
          #self.refreshVMList()


    ## Slot with file dialog, for selct a dir.
    @pyqtSlot()
    def selectUserDir(self):
        #print "selectUserDir()"
        dirname = QtGui.QFileDialog.getExistingDirectory(self, "Select home dir", self.userDirLineEdit.text(),QtGui.QFileDialog.ShowDirsOnly)
        self.userDirLineEdit.setText(dirname)


    ## Slot for safe edits
    @pyqtSlot()
    def safeEdits(self):       
	print "[safe edits...]"
	
	
