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


import os

## @file KVMManager.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## Class handling KVM commands.
class KVMManager():

    def commandTest(self):
        _command = "ls"
        _ausgabe = os.system(_command)
        print "[commanttest] 1): ", _ausgabe
        _command = "cat ./vghvhjg.txt"
        _ausgabe = os.system(_command)
        print "[commanttest] 2): ", _ausgabe
        _command = "ls"
        _ausgabe = os.popen4(_command)
        print "[commanttest] 3): ", _ausgabe
        _command = "cat ./vghvhjg.txt"
        _ausgabe = os.popen4(_command)
        print "[commanttest] 4): ", _ausgabe