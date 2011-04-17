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

import time
import sys
import logging
import sqlite3
import os.path
import subprocess

from datetime import date
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot

from CloneVMWindow import CloneVMWindow
from ConfigVMWindow import ConfigVMWindow
from DetailInfoDialog import DetailInfoDialog
from InstallMediaWindow import InstallMediaWindow
from KVMManager import KVMManager
from MainConfigWindow import MainConfigWindow
from NewVMWindow import NewVMWindow
from UserWindow import UserWindow
from VMinfo import VMinfo
from VMinfoDB import VMinfoDB 
from GLOBALS import BASEDIR, ICONDIR, FRAM_STYLE_SHEET

## @file MainWindow.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## The main window of the GUI
class MainWindow(QtGui.QMainWindow):

    ## Frame style
    __owneFramStyleSheet = FRAM_STYLE_SHEET    

    ## Simple List
    __listview = ""

    ## Save information about vitual machines
    __vmInfoDB = VMinfoDB()

    ## Managet KVM comands
    #__kvmManager = KVMManager()
    
    ## order of VM list.
    __listOrder = QtCore.Qt.DescendingOrder

    ## Constructor
    def __init__(self, *args): 
        QtGui.QMainWindow.__init__(self, *args)


        logging.debug('init main window....')

        self.resize(800,600)
        self.setWindowTitle('Isar')
        self.setStyleSheet(self.__owneFramStyleSheet)


        #---------- menubar --------------------
        
        #---------- file menu ---------------------

        menubar = self.menuBar()
        menuFile = menubar.addMenu('&File')        

        # Menue-item for init the database.
        menuInitDB = QtGui.QAction( 'Create Database', self)
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
        menuEditISO.setShortcut('Ctrl+M')
        menuEditISO.setStatusTip('Edit and configure instal media.')
        self.connect(menuEditISO, QtCore.SIGNAL('triggered()'), QtCore.SLOT('editISOs()'))
        menuFile.addAction(menuEditISO)
        
        menuFile.addSeparator()

        # Menue-item for main config.
        menuEditConf = QtGui.QAction( 'Settings', self)
        menuEditConf.setShortcut('Ctrl+C')
        menuEditConf.setStatusTip('Edit and configure instal media.')
        self.connect(menuEditConf, QtCore.SIGNAL('triggered()'), QtCore.SLOT('mainConfig()'))
        menuFile.addAction(menuEditConf)        
        
        ## Menue-item for apliction exit
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'exit.png'))
        menuExit = QtGui.QAction(_icon, 'Exit', self)
        menuExit.setShortcut('Ctrl+Q')
        menuExit.setStatusTip('Exit application')
        self.connect(menuExit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        menuFile.addAction(menuExit)
        
        # ----------- virtual machine menue
        menuMachine = menubar.addMenu('Machines')          

        # Create a new virtual machine.
        menuMachineNew = QtGui.QAction( 'New', self)
        menuMachineNew.setShortcut('Ctrl+N')
        menuMachineNew.setStatusTip('Create a new virtual machine.')
        self.connect(menuMachineNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('newVMDialog()'))
        menuMachine.addAction(menuMachineNew)
        
        # Delete a virtual machine
        menuMachineDelete = QtGui.QAction( 'Delete', self)
        menuMachineDelete.setShortcut('Ctrl+X')
        menuMachineDelete.setStatusTip('Delete a virtual machine')
        self.connect(menuMachineDelete, QtCore.SIGNAL('triggered()'), QtCore.SLOT('deleteVM()'))
        menuMachine.addAction(menuMachineDelete)

        # view all exist virtual machine
        menuViewExist = QtGui.QAction( 'View all exist', self)
        menuViewExist.setShortcut('Ctrl+V')
        menuViewExist.setStatusTip('View all exist virtual machine')
        self.connect(menuViewExist, QtCore.SIGNAL('triggered()'), QtCore.SLOT('viewAllExistVM()'))
        menuMachine.addAction(menuViewExist)     
        
        
        # import all exist virtual machine, where missing in Database.
        menuImportExist = QtGui.QAction( 'Import exist machine', self)
        menuImportExist.setShortcut('Ctrl+Y')
        menuImportExist.setStatusTip('Import all exist virtual machine, where missing in Database')
        self.connect(menuImportExist, QtCore.SIGNAL('triggered()'), QtCore.SLOT('importAllExistVM()'))
        menuMachine.addAction(menuImportExist)
        
        # --------- info menu ---------------

        menuInfo = menubar.addMenu('&Info')        

        ## Menue-item for about dialog.
        menuInfoAbout = QtGui.QAction( 'About', self)
        menuInfoAbout.setShortcut('Ctrl+I')
        menuInfoAbout.setStatusTip('About this programm.')
        self.connect(menuInfoAbout, QtCore.SIGNAL('triggered()'), QtCore.SLOT('about()'))
        menuInfo.addAction(menuInfoAbout)

        # ------------- menu end ------------

        # ----------- toolbar ---------------------
        self.toolbar = self.addToolBar('tools')

        # Tool button new virtual machine
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'new.png'))
        toolNew = QtGui.QAction(_icon, 'Create a new virtual machine', self)
        toolNew.setShortcut('Ctrl+N')
        self.connect(toolNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('newVMDialog()'))
        self.toolbar.addAction(toolNew)

        # Tool button delete a virtual machine
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'remove.png'))
        toolRemove = QtGui.QAction(_icon, 'Delete a virtual machine', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolRemove, QtCore.SIGNAL('triggered()'), QtCore.SLOT('deleteVM()'))
        self.toolbar.addAction(toolRemove)

        # Tool button clone a virtual machine
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'clone.png'))
        toolClone = QtGui.QAction(_icon, 'Clone a virtual machine', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolClone, QtCore.SIGNAL('triggered()'), QtCore.SLOT('cloneVMDialog()'))
        self.toolbar.addAction(toolClone)


        # Separator ----------------------------
        self.toolbar.addSeparator()

        # Tool button info of virtual machine
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'info.png'))
        toolInfo = QtGui.QAction(_icon, 'Info of virtual machine', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolInfo, QtCore.SIGNAL('triggered()'), QtCore.SLOT('infoVM()'))
        self.toolbar.addAction(toolInfo)

        # Tool button start virtual machine
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'vmstart.png'))
        toolVMstart = QtGui.QAction(_icon, 'Start a virtual machine', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolVMstart, QtCore.SIGNAL('triggered()'), QtCore.SLOT('startVM()'))
        self.toolbar.addAction(toolVMstart)

        # Tool button stop a virtual machine
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'vmstop.png'))
        toolVMstop = QtGui.QAction(_icon, 'Stop a virtual machine', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolVMstop, QtCore.SIGNAL('triggered()'), QtCore.SLOT('stopVM()'))
        self.toolbar.addAction(toolVMstop)

        # Tool button view a running virtual machine.
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'viewvm.png'))
        toolViewVM = QtGui.QAction(_icon, 'View a running virtual machine', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolViewVM, QtCore.SIGNAL('triggered()'), QtCore.SLOT('viewVM()'))
        self.toolbar.addAction(toolViewVM)        
        
        # Separator -----------------------------------------
        self.toolbar.addSeparator()

        # Tool button Edit user
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'user.png'))
        toolUser = QtGui.QAction(_icon, 'Edit user', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolUser, QtCore.SIGNAL('triggered()'), QtCore.SLOT('editUser()'))
        self.toolbar.addAction(toolUser)

        # Tool button
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'isoinfo.png'))
        toolISOs = QtGui.QAction(_icon, 'Edit and configure instal media.', self)
        toolISOs.setShortcut('Ctrl+X')
        self.connect(toolISOs, QtCore.SIGNAL('triggered()'), QtCore.SLOT('editISOs()'))
        self.toolbar.addAction(toolISOs)        
        
        
        # Separator -----------------------------------------
        self.toolbar.addSeparator()

        # Tool button Edit user
        _icon = QtGui.QIcon(os.path.join(ICONDIR + 'configure.png'))
        toolConf = QtGui.QAction(_icon, 'Edit user', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolConf, QtCore.SIGNAL('triggered()'), QtCore.SLOT('mainConfig()'))
        self.toolbar.addAction(toolConf)        
        
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

        self.__listview = QtGui.QTreeWidget()
        #self.__listview.setSortingEnabled(True)
        _haderList = ["owner","name","create","OS"]
        self.__listview.setColumnCount(len(_haderList))
        (self.__listview.header()).resizeSection(0, 130) 
        (self.__listview.header()).resizeSection(1, 190) 
        (self.__listview.header()).resizeSection(2, 130) 
        (self.__listview.header()).resizeSection(3, 130) 
        self.__listview.setHeaderLabels(_haderList)
        #self.connect(self.__listview,
            QtCore.SIGNAL('doubleClicked(QModelIndex*,int)'), QtCore.SLOT('self.viewVM'))
        self.connect(self.__listview, QtCore.SIGNAL('mouseDoubleClickEvent()'), QtCore.SLOT('viewVM()'))
        vListLayoutL.addWidget(self.__listview)
        # ---------- Statusbar ------------
        self.statusBar().showMessage('...Ready')
        # Item-List
        self.refreshVMList()

    ## A function with qt-slot. it's sorted the list of VMs.
    #@pyqtSlot()
    #def sortList(self):
        #_index = self.__listview.currentColumn()
        #print "[_index]: ", _index
        #if self.__listOrder == QtCore.Qt.DescendingOrder:
            #self.__listview.sortItems(_index, QtCore.Qt.AscendingOrder)
            #self.__listOrder = QtCore.Qt.AscendingOrder
        #else:
            #self.__listview.sortItems(_index, QtCore.Qt.DescendingOrder)
            #self.__listOrder = QtCore.Qt.DescendingOrder
            

    ## A function with qt-slot. it's creade a new vm.
    @pyqtSlot()
    def newVMDialog(self):
        print "[newVMDialog] editUser"
        try:
            nvm = NewVMWindow(self.__vmInfoDB)
            nvm.setModal(True)
            nvm.show()
            ret = nvm.exec_()
        except sqlite3.Error, e: 
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
            return        
        self.refreshVMList()
      

        
    ## Refrash the list of tasks.
    @pyqtSlot()
    def refreshVMList(self):
        _VMList = list()
        try:
            _VMList = self.__vmInfoDB.getAllVMinfo()
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
            return            
        self.__listview.clear()
        for item in _VMList:
            _date = d = date.fromtimestamp(int(item.createdate))
            qStringList = QtCore.QStringList([ \
                str(item.owner),  \
                str(item.name),  \
                str(_date.strftime("%d.%m.%Y")),  \
                str(item.os) \
            ])
            twItem = QtGui.QTreeWidgetItem(qStringList)
            self.__listview.addTopLevelItem(twItem)



    ## Function clone a vm
    @pyqtSlot()
    def cloneVMDialog(self):
        logging.debug("[201104101758] cloneVMDialog")
        _vmName = ""
        for item in self.__listview.selectedItems():
            print  "[...]" , item.text(1)
            _vmName = str(item.text(1))
            _distName = str(item.text(3))

        if( _vmName == "" ):
            self.statusBar().showMessage('No ToDo select...')
            QtGui.QMessageBox.information(self, "Abort",'No virtual machine select!')
            return
        
        print "[_vmName]", _vmName

        try:
            _cvm = CloneVMWindow(self.__vmInfoDB)
            _cvm.setOriginalVM(_vmName)
            _cvm.setDistName(_distName)
            _cvm.setModal(True)
            _cvm.show()
            ret = _cvm.exec_()
        except sqlite3.Error, e: 
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
            return
        self.refreshVMList()
        return        

    ## Function show or eding info of vm
    @pyqtSlot()
    def doubleClicked(self,item, column):
        print "[doubleClicked]"
        self.infoVM()

    ## Function show or eding info of vm
    @pyqtSlot()
    def infoVM(self):
        logging.debug("[infoVM] ...")
        _vmName = ""
        for item in self.__listview.selectedItems():
            print  "[...]" , item.text(1)
            _vmName = str(item.text(1))

        if( _vmName == "" ):
            self.statusBar().showMessage('No virtual machine select...')
        else:
            print "[_vmName]", _vmName
            try:
                _cvm = ConfigVMWindow(self.__vmInfoDB, _vmName)
                _cvm.setModal(True)
                _cvm.show()
                ret = _cvm.exec_()
            except sqlite3.Error, e: 
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.critical(self, "Error", str(infotext))
                return          
            
            self.refreshVMList()
            return     

    ## Function start a virtual machine
    @pyqtSlot()
    def startVM(self):
        logging.debug("[startVM] ...")
        _vmName = ""
        for item in self.__listview.selectedItems():
            _vmName = str(item.text(1))

        if( _vmName == "" ):
            infotext = 'No virtual machine select...'
            self.statusBar().showMessage(infotext)
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
        else:
            print "[_vmName:]", _vmName
            try:
                _kvmManager = KVMManager()
                _result = _kvmManager.startMachine(_vmName)
                QtGui.QMessageBox.information(self, "Result", _result)
            except subprocess.CalledProcessError, e:
                infotext = "An error occurred:", (e.output.replace('\n',' ')).replace('\r',' ')
                QtGui.QMessageBox.critical(self, "Error", str(infotext))
                return

    ## Function stop a virtual machine
    @pyqtSlot()
    def stopVM(self):
        logging.debug("[stopVM] ...")
        _vmName = ""
        for item in self.__listview.selectedItems():
            _vmName = str(item.text(1))

        if( _vmName == "" ):
            infotext = 'No virtual machine select...'
            self.statusBar().showMessage(infotext)
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
        else:
            print "[_vmName:]", _vmName
            try:
                _kvmManager = KVMManager()
                _result = _kvmManager.stopMachine(_vmName)
                QtGui.QMessageBox.information(self, "Result", _result)
            except subprocess.CalledProcessError, e:
                infotext = "An error occurred:", (e.output.replace('\n',' ')).replace('\r',' ')
                QtGui.QMessageBox.critical(self, "Error", str(infotext))
                return


    ## Function view a virtual machine
    @pyqtSlot()
    def viewVM(self):
        logging.debug("[viewVM] ...")
        _vmName = ""
        for item in self.__listview.selectedItems():
            _vmName = str(item.text(1))

        if( _vmName == "" ):
            infotext = 'No virtual machine select...'
            self.statusBar().showMessage(infotext)
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
        else:
            print "[_vmName:]", _vmName
            try:
                _kvmManager = KVMManager()
                _result = _kvmManager.viewMachine(_vmName)
                #QtGui.QMessageBox.information(self, "Result", _result)
            except subprocess.CalledProcessError, e:
                infotext = "An error occurred:", (e.output.replace('\n',' ')).replace('\r',' ')
                QtGui.QMessageBox.critical(self, "Error", str(infotext))
                return



    ## Function delete a vm
    @pyqtSlot()
    def deleteVM(self):
        logging.debug("[20110402201311] deleteVM")
        _infotext = "Do you want to delete this machine? \n"
        _infotext += "Has only effect for isar data base. Not for Libvirt."
        ret = QtGui.QMessageBox.warning(self, \
                            "Warning", \
                            _infotext, \
                            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)

        if (ret == QtGui.QMessageBox.Cancel):
            return

        _vmName = ""
        for item in self.__listview.selectedItems():
            print  ".." , item.text(1)
            _vmName = str(item.text(1))

        if( _vmName == "" ):
            self.statusBar().showMessage('No ToDo select...')
            QtGui.QMessageBox.information(self, "Abort",'No virtual machine select!')
            return
        
        print "[_vmName]", _vmName
        try:              
            self.__vmInfoDB.deleteVMinfo(_vmName)
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error",str(infotext))
            return  
        self.refreshVMList()


        
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
        self.__vmInfoDB.initDB()


    ## Slot for open eding user window.
    @pyqtSlot()
    def editUser(self):
        logging.debug("[20110403172927] editUser")
        print "[20110403172927] editUser"     
        try:
            uw = UserWindow(self.__vmInfoDB)
            uw.setModal(True)
            uw.show()
            ret = uw.exec_()
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
            return
        print "[20110403182643] editUser"     


    ## Slot for open  window for eding instal ISO liste.
    @pyqtSlot()
    def editISOs(self):
        logging.debug("[20110403172927] editISOs")
        print "[20110403172927] editISOs"
        try:
            _imw = InstallMediaWindow(self.__vmInfoDB)
            _imw.setModal(True)
            _imw.show()
            ret = _imw.exec_()
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
            return

    ## Slot for open  window for eding main config.
    @pyqtSlot()
    def mainConfig(self):
        logging.debug("[mainConfig]")
  
        print "[mainConfig]"
        try:
            _mcw = MainConfigWindow(self.__vmInfoDB)
            _mcw.setModal(True)
            _mcw.show()
            ret = _mcw.exec_()
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
            return

    ## Slot for open  window for eding main config.
    @pyqtSlot()
    def viewAllExistVM(self):
        logging.debug("[viewAllExistVM]")
        _kvmManager = KVMManager()    
        _infotext = _kvmManager.getAllExistVM()
                
        _did = DetailInfoDialog()
        _did.setText("Result:")
        _did.setDetailedText(str(_infotext))
        _did.exec_()        
        self.close()
        

    ## Slot for open  window for eding main config.
    @pyqtSlot()
    def importAllExistVM(self):
        logging.debug("[importAllExistVM]")
        _kvmManager = KVMManager()    
        _infotext = _kvmManager.getAllExistVM()
        _vmInfo = VMinfo()
        _importVMList = list()
        _VMList = list()
        try:
            _VMList = self.__vmInfoDB.getAllVMinfo()
        except sqlite3.Error, e:
            infotext = "An error occurred:", e.args[0]
            QtGui.QMessageBox.critical(self, "Error", str(infotext))
            return    
            
        print "_infotext", len(_infotext.split("\n"))
        _lines = _infotext.split("\n")
        # cute list header..
        _netto = _lines[2:]
        # if exist virtual machine...
        for _line in _netto:
            _columns = _line.split(" ")
            # if exist virtual machine...
            if len(_columns) > 3:
                _existVMName = _columns[3]
                # comparing data base list with list of exist machines.
                _isFoundInDB = False
                for _dbItem in _VMList:
                    if str(_dbItem.name) == str(_existVMName):
                        print "[ignore]:", str(_dbItem.name)
                        _isFoundInDB = True
                # disregard if name in database of isar
                if _isFoundInDB == False:
                    _importVMList.append(_existVMName)
        # Import...
        for _vmName in _importVMList:
            
            _vmInfo.name = _vmName
            _vmInfo.createdate = str(int(time.time()))
            _vmInfo.lifetimedays = "60"
            _vmInfo.comment = "Data import by isar." 
            _vmInfo.mail = "root@localhost"
            _vmInfo.image_file = ""
            _vmInfo.owner = "no body"
            _vmInfo.OS = "unknown"
        
            try:
                self.__vmInfoDB.addVMinfo(_vmInfo)
            except sqlite3.Error, e:
                infotext = "An error occurred:", e.args[0]
                QtGui.QMessageBox.critical(self, "Error",str(infotext))
                return              
            
        _did = DetailInfoDialog()
        _did.setText("Import:")
        _did.setDetailedText("\n".join(_importVMList))
        _did.exec_()     
        self.refreshVMList()    
        