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
import shlex, subprocess

## @file KVMManager.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## Class handling KVM commands.
class KVMManager():

    def commandTest(self):
        #_command = "ls"
        #_ausgabe = os.system(_command)
        #print "[commanttest] 1): ", _ausgabe
        #_command = "cat ./vghvhjg.txt"
        #_ausgabe = os.system(_command)
        #print "[commanttest] 2): ", _ausgabe
        #_command = "ls"
        #_ausgabe = os.popen4(_command)
        #print "[commanttest] 3): ", _ausgabe
        #_command = "cat ./vghvhjg.txt"
        #_ausgabe = os.popen4(_command)
        #print "[commanttest] 4): ", _ausgabe
        #_command = "ls"
        #print "[commanttest] 5) check_output: ", subprocess.check_output(_command)
        #print "[commanttest] 5) check_output: ", subprocess.check_output(["cat", "./vghvhjg.txt"])
 
 
        _dummy, _f = os.popen4('ls')
        _out = ""
        for _line in _f:
            print "[commanttest] 5) _line: ", _line
            _out = _out + _line
        print "[commanttest] 5) _out: >>" , _out, "<<"

        #_dummy, _f = os.popen4('cat ./vghvhjg.txt')
        #_out = ""
        #for _line in _f:
            #print "[commanttest] 6) _line: ", _line
            #_out = _out + _line
        #print "[commanttest] 6) _out: >>" , _out, "<<"
        
        return  _out