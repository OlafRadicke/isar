#!/usr/bin/python
# -*- coding: utf-8 -*-


 ###########################################################################
 #   Copyright (C) 2010 by Olaf Radicke                                    #
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
from datetime import datetime, date, time
from PyQt4 import QtGui, QtCore
from gui.MainWindow import MainWindow


## @file GUI.py
# @author Olaf Radicke<radicke@atix.de>

#LOG_FILENAME = '/tmp/isar.log'
LOG_FILENAME = 'isar.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
_startinfo = '============= Start ' + datetime.now().strftime("%d. %B %Y %H:%M") + ' ==============='
logging.debug(_startinfo)


def startGUI():
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

startGUI()
sys.exit(0)