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
from UserWindow import UserWindow
from InstallMediaWindow import InstallMediaWindow
from NewVMWindow import NewVMWindow

## @file MainWindow.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## The main window of the GUI
class MainWindow(QtGui.QMainWindow):


    ## Simple List
    listview = ""

    ## TaskView: This class show the taskt data.
    taskBox = ""

    ## Minutes of the proceedings as html
    minutes =  ""


    ## This QTextBrowser show the minutes of the proceedings
    textView = ""

    ## Save information about vitual machines
    vmInfoDB = VMinfoDB()

    ## Constructor
    def __init__(self, *args): 
        QtGui.QMainWindow.__init__(self, *args)


        logging.debug('init main window....')

        self.resize(800,600)
        self.setWindowTitle('Isar')


        #---------- menubar --------------------
        

        menubar = self.menuBar()
        menuFile = menubar.addMenu('&File')        



        # Menue-item for init the database.
        menuInitDB = QtGui.QAction( 'Init Database', self)
        menuInitDB.setShortcut('Ctrl+D')
        menuInitDB.setStatusTip('Init the SQLite3-Database.')
        self.connect(menuInitDB, QtCore.SIGNAL('triggered()'), QtCore.SLOT('initDB()'))
        menuFile.addAction(menuInitDB)


        # Menue-item for Edit and configure user info.
        menuEditUser = QtGui.QAction( 'Edit user', self)
        menuEditUser.setShortcut('Ctrl+U')
        menuEditUser.setStatusTip('Edit and configure user info.')
        self.connect(menuEditUser, QtCore.SIGNAL('triggered()'), QtCore.SLOT('editUser()'))
        menuFile.addAction(menuEditUser)



        # Menue-item for Edit and configure install ISOs.
        menuEditISO = QtGui.QAction( 'Edit instal ISOs', self)
        menuEditISO.setShortcut('Ctrl+U')
        menuEditISO.setStatusTip('Edit and configure instal media.')
        self.connect(menuEditISO, QtCore.SIGNAL('triggered()'), QtCore.SLOT('editISOs()'))
        menuFile.addAction(menuEditISO)
        
        ## Menue-item for apliction exit
        menuExit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        menuExit.setShortcut('Ctrl+Q')
        menuExit.setStatusTip('Exit application')
        self.connect(menuExit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        menuFile.addAction(menuExit)

        ## Menue-item for about dialog.
        menuInfoAbout = QtGui.QAction( 'About', self)
        menuInfoAbout.setShortcut('Ctrl+I')
        menuInfoAbout.setStatusTip('About this programm.')
        self.connect(menuInfoAbout, QtCore.SIGNAL('triggered()'), QtCore.SLOT('about()'))


        menuFile = menubar.addMenu('&Info')
        menuFile.addAction(menuInfoAbout)

        # ------------- menu end ------------

        # ----------- toolbar ---------------------
        self.toolbar = self.addToolBar('tools')
        
        toolNew = QtGui.QAction(QtGui.QIcon('./icons/new.png'), 'Create a new virtual machine', self)
        toolNew.setShortcut('Ctrl+N')
        self.connect(toolNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('newVMDialog()'))
        self.toolbar.addAction(toolNew)

        toolRemove = QtGui.QAction(QtGui.QIcon('./icons/remove.png'), 'Delete a virtual machine', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolRemove, QtCore.SIGNAL('triggered()'), QtCore.SLOT('deleteVM()'))
        self.toolbar.addAction(toolRemove)


        toolInfo = QtGui.QAction(QtGui.QIcon('./icons/info.png'), 'Info of virtual machine', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolInfo, QtCore.SIGNAL('triggered()'), QtCore.SLOT('infoVM()'))
        self.toolbar.addAction(toolInfo)


        toolClone = QtGui.QAction(QtGui.QIcon('./icons/clone.png'), 'Info of virtual machine', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolClone, QtCore.SIGNAL('triggered()'), QtCore.SLOT('cloneVM()'))
        self.toolbar.addAction(toolClone)     
        # ----------- toolbar end ------------------------



        ## Main Widget
        centralWidget = QtGui.QWidget()
        self.setCentralWidget(centralWidget)

        ## Main layout V
        vMainLayout = QtGui.QVBoxLayout()
        centralWidget.setLayout(vMainLayout)
        
        ## Main layout H
        hMainLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hMainLayout)


        # ----------- Left box ---------------------------------

        # VBox left with GrouBox-frame
        listBox = QtGui.QGroupBox("VM list")
        listBox.setMaximumWidth(800)
        vListLayoutL = QtGui.QVBoxLayout()
        listBox.setLayout(vListLayoutL)
        hMainLayout.addWidget(listBox)
        

        # -------------- List --------------

        self.listview = QtGui.QTreeWidget()
        _haderList = ["owner","name","create","OS"]
        self.listview.setColumnCount(len(_haderList))
        self.listview.setHeaderLabels(_haderList)
        vListLayoutL.addWidget(self.listview)
        #self.listview.addTopLevelItem( QtGui.QTreeWidgetItem(["Olaf","CluterTest","2011-03-29","2011-05-31","fedora13"]))

        # ---------- Statusbar ------------
        self.statusBar().showMessage('Ready')
        # Item-List
        self.refreshVMList()


    ## A function with qt-slot. it's creade a new vm.
    @pyqtSlot()
    def newVMDialog(self):
        print "[newVMDialog] editUser"
        try:
            nvm = NewVMWindow(self.vmInfoDB)
            nvm.show()
            ret = nvm.exec_()
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.information(self, "Error", str(infotext))
            return
        self.refreshVMList()
      

        
    ## Refrash the list of tasks.
    @pyqtSlot()
    def refreshVMList(self):
        userList = list()
        try:
            userList = self.vmInfoDB.getAllVMinfo()
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.information(self, "Error", str(infotext))
            return            
        self.listview.clear()
        for item in userList:
            qStringList = QtCore.QStringList([ \
                str(item.owner),  \
                str(item.name),  \
                str(item.createdate),  \
                str(item.os) \
            ])
            twItem = QtGui.QTreeWidgetItem(qStringList)
            self.listview.addTopLevelItem(twItem)



    ## Function clone a vm
    @pyqtSlot()
    def cloneVM(self):
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

    ## Function show info of vm
    @pyqtSlot()
    def infoVM(self):
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

    ## Function delete a vm
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


        
    ## Open about-dialog
    @pyqtSlot()
    def about(self):
        infotext = "Working title: Isar \n"
        infotext = infotext + "Lizenz: GPL3 \n"
        infotext = infotext + "URL: https://github.com/OlafRadicke/isar \n"
        infotext = infotext + "Contact: Olaf Radicke <briefkasten@olaf-radicke.de>"

        QtGui.QMessageBox.information(self, "About",infotext)
      

    ## Slot for init database.
    @pyqtSlot()
    def initDB(self):
        logging.debug("[20110402220213] init db")
        print "[20110402220213] init db"
        self.vmInfoDB.initDB()


    ## Slot for open eding user window.
    @pyqtSlot()
    def editUser(self):
        logging.debug("[20110403172927] editUser")
        print "[20110403172927] editUser"     
        try:
            uw = UserWindow(self.vmInfoDB)
            uw.show()
            ret = uw.exec_()
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.information(self, "Error", str(infotext))
            return
        print "[20110403182643] editUser"     


    ## Slot for open  window for eding instal ISO liste.
    @pyqtSlot()
    def editISOs(self):
        logging.debug("[20110403172927] editISOs")
        print "[20110403172927] editISOs"
        try:
            _imw = InstallMediaWindow(self.vmInfoDB)
            _imw.show()
            ret = _imw.exec_()
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.information(self, "Error", str(infotext))
            return