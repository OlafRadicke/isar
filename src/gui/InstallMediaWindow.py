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
import os.path
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from VMinfoDB import VMinfoDB 
from UserInfo import UserInfo
from GLOBALS import ICONDIR, FRAM_STYLE_SHEET


## @file installMediaWindow.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## The window view info about install ISOs.
class InstallMediaWindow(QtGui.QDialog):
  
    ## Frame style
    __owneFramStyleSheet = FRAM_STYLE_SHEET    

  
    ## Database binding.
    __vmInfoDB = VMinfoDB()

    ## Simple List
    listview = ""
    
    __isoPathName = ""
    
    ## path of install Media. Is a QLineEdit class.
    isoPathLineEdit = ""

    ## Button for select a path
    isoPathPushButton = ""
    
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
        self.setStyleSheet(self.__owneFramStyleSheet)

        ## Main layout V
        vMainLayout = QtGui.QVBoxLayout()
        #centralWidget.setLayout(vMainLayout)
        self.setLayout(vMainLayout)
        
        ## Main layout H
        hMainLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hMainLayout)


        # ----------- Left box ---------------------------------

        # VBox left with GrouBox-frame
        listBox = QtGui.QGroupBox("list of install medias")
        listBox.setMaximumWidth(600)
        vListLayoutL = QtGui.QVBoxLayout()
        listBox.setLayout(vListLayoutL)
        hMainLayout.addWidget(listBox)
        

        # -------------- List --------------

        self.listview = QtGui.QTreeWidget()
        _haderList = ["ISOs"]
        self.listview.setColumnCount(len(_haderList))
        self.listview.setHeaderLabels(_haderList)
        vListLayoutL.addWidget(self.listview)
        self.connect \
        ( \
            self.listview, \
            QtCore.SIGNAL('itemSelectionChanged()'), \
            QtCore.SLOT('fillDetailView()') \
        )
        #self.connect(self.listview, QtCore.SIGNAL('clicked()'), QtCore.SLOT('fillDetailView()'))

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
        isoPathLabel = QtGui.QLabel("Path of install ISO:")
        hLayoutUserDir.addWidget(isoPathLabel)
        self.isoPathLineEdit = QtGui.QLineEdit()
        self.isoPathLineEdit.setReadOnly(True)
        hLayoutUserDir.addWidget(self.isoPathLineEdit)
        self.isoPathPushButton = QtGui.QPushButton() #":/")
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'search.png'))        
        self.isoPathPushButton.setIcon(_icon)
        # self.isoPathPushButton.setReadOnly(True)
        self.connect(self.isoPathPushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('selectISOpath()'))
        hLayoutUserDir.addWidget(self.isoPathPushButton)        
        

        # Save buttom
        hSefeLayout = QtGui.QHBoxLayout()
        vEditLayoutR.addLayout(hSefeLayout)
        
        saveButton = QtGui.QPushButton("Save Edits")
        self.connect(saveButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('saveEdits()'))
        hSefeLayout.addWidget(saveButton) 
        
        
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
        
        self.refreshISOList()

    ## Slot delete user.
    @pyqtSlot()
    def deleteISOpath(self):
        print "[delete ISO path...]"
        _name = ""

        ret = QtGui.QMessageBox.warning(self, \
                            "Warning", \
                            "Do you want to delete this entry?", \
                            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)

        if (ret == QtGui.QMessageBox.Cancel):
            print "...cencel"
            return
        elif (ret == QtGui.QMessageBox.Ok):
            print "...Ok"
        
        for item in self.listview.selectedItems():
            print  ".." , item.text(0)
            _name = item.text(0)

        if str(_name) == "":
              infotext = "No user select!"
              QtGui.QMessageBox.critical(self, "Error",str(infotext))
              return
        else:
            try:
                self.__vmInfoDB.deleteISOpath(str(_name))
            except sqlite3.Error, e:
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.critical(self, "Error",str(infotext))
                return

            self.refreshISOList()
          
    ## Slot delete user.
    @pyqtSlot()
    def fillDetailView(self):
        #print "[fillDetailView...]"
        _name = ""
        _listIsEmpty = True
        for item in self.listview.selectedItems():
            _listIsEmpty = False
            #print  "[...]" , item.text(0)
            _name = item.text(0)
        if _listIsEmpty:
            return
        if str(_name) == "":
              infotext = "No entry select!"
              QtGui.QMessageBox.critical(self, "Error",str(infotext))
              return
        else:
            try:
                _path = self.__vmInfoDB.getISOpath(str(_name))               
            except sqlite3.Error, e:
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.critical(self, "Error",str(infotext))
                return
            if _path == -1 or _path == None:
                print "[20110405234854] _path.' ", _path
                infotext = "ISO name not found!"
                QtGui.QMessageBox.critical(self, "Error",str(infotext))
                return
            else:
                print "[] _path: ", _path
                self.isoPathLineEdit.setText( _path )
                self.isoPathLineEdit.setReadOnly(False)

            self.isoPathLineEdit.setReadOnly(False)
            # self.isoPathPushButton.setReadOnly(False)
          
    ## A function with qt-slot. it's creade a new vm.
    @pyqtSlot()
    def newISOpathDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, "New ISO path", "Label name (not path):", 0)
        if ok != True :
            logging.debug("[201104] if: " + str(text) + str(ok))
            return
        else:
            logging.debug("[20110411] else: " + str(text) + str(ok))
            print "[2011042] else: " + str(text)
            try:
                self.__vmInfoDB.addISOpath(str(text))
            except sqlite3.Error, e:
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.critical(self, "Error",str(infotext))
                return

            self.__isoPathName = str(text)
            self.refreshISOList()
      

        
    ## Refrash the list of tasks.
    @pyqtSlot()
    def refreshISOList(self):
        print "[refreshISOList]"
        nameList = self.__vmInfoDB.getAllISOnames()
        self.listview.clear()
        for item in nameList:
            qStringList = QtCore.QStringList( [ str(item) ] )
            #twItem = QtGui.QTreeWidgetItem(qStringList)
            twItem = QtGui.QTreeWidgetItem(QtCore.QStringList(item))
            self.listview.addTopLevelItem(twItem)
            
        self.isoPathLineEdit.setReadOnly(True)
        # self.isoPathPushButton.setReadOnly(True)


    ## Slot for save edits
    @pyqtSlot()
    def saveEdits(self):       
        print "[save edits...]"
        _name = ""
        for item in self.listview.selectedItems():
            print  ".." , item.text(0)
            _name = item.text(0)

        if str(_name) == "":
              infotext = "No entry select!"
              QtGui.QMessageBox.critical(self, "Error",str(infotext))
              return
        try:
            self.__vmInfoDB.updateISOpath(str(_name), str(self.isoPathLineEdit.text()))
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error",str(infotext))
            return
        infotext = "Ok, saved..."
        QtGui.QMessageBox.information(self, "OK",str(infotext))

    ## Slot with file dialog, for selct a dir.
    @pyqtSlot()
    def selectISOpath(self):
        #print "selectISOpath()"
        dirname = QtGui.QFileDialog.getOpenFileName(self, "Select ISO image", "","ISO(*.iso *.ISO);; all(*.*)")
        self.isoPathLineEdit.setText(dirname)

  