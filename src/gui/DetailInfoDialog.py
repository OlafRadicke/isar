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


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot



## @file DetailInfoDialog.py
# @author serge_gubenko
# original source: http://stackoverflow.com/questions/2655354/how-to-allow-resizing-of-qmessagebox-in-pyqt4

# Using example:
# mb = DetailInfoDialog()
# mb.setText("Hallo:")
# mb.setDetailedText('...wold!')
# mb.exec_()

## This dialo get user big infos.
class DetailInfoDialog(QtGui.QMessageBox):
    def __init__(self):
        QtGui.QMessageBox.__init__(self)
        self.setSizeGripEnabled(True)
        textEdit = self.findChild(QtGui.QTextEdit)
        if textEdit != None :
            textEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

    def event(self, e):
        result = QtGui.QMessageBox.event(self, e)

        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(300)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        textEdit = self.findChild(QtGui.QTextEdit)
        if textEdit != None :
            textEdit.setMinimumHeight(400)
            textEdit.setMaximumHeight(16777215)
            textEdit.setMinimumWidth(400)
            textEdit.setMaximumWidth(16777215)
            textEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        return result
    