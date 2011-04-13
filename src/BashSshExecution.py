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
        print "[Command]:",_command
        _command = "ssh -Y " + self.sshUser + "@" + self.address \
            + " \"" + _command + "\""
            
        _f = subprocess.check_output(_command.split(),stderr=subprocess.STDOUT)
        _out = ""
        print "[_f]", _f
        for _line in _f:
            _out = _out + _line
        return  _out    