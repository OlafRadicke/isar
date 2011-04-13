#! /usr/bin/env python
# -*- coding: utf-8 -*-

##
#    Copyright (C) 2011  Olaf Radicke
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import shlex, subprocess

## @file BashSshExecution.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## Class for execute commands in a ssh.
class BashSshExecution:

    ## ssh-server address
    address = ""

    ## ssh-user name
    sshUser = ""

    ## Constructor.
    def __init__(self):
        pass

    ## execute a bash command.
    # @return Return result.
    # except: subprocess.CalledProcessError
    def do(self, _command):
        _commantList = list()
        _commantList.append("ssh")
        _commantList.append("-Y")
        _commantList.append(self.sshUser + "@" + self.address)
        _commantList.append(_command)
        #_command = " -Y " + self.sshUser + "@" + self.address \
            #+ " \"" + _command + "\""
        print "[ssh Command]:", _commantList
        _f = subprocess.check_output(_commantList,stderr=subprocess.STDOUT)
        _out = ""
        print "[_f]", _f
        for _line in _f:
            _out = _out + _line
        return  _out    