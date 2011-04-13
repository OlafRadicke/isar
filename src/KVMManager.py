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
from BashSshExecution import BashSshExecution

## @file KVMManager.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## Class handling KVM commands.
class KVMManager():
    
    
    ## Nickname of owners home dir
    __ownersHome = "XX"
    
    ## Name of virtual machine
    __vmName = "XX"
    
    ## size of RAM (mb)
    __ram = "1000"
    
    ## size of hard disc (Gb).
    __hdSize = "1000"
    
    ## Path of install ISO
    __IsoPath = ""
    

    ## Name of original virtual machine
    # For clone command.
    __originalVM = ""  
    
    ## Path of virtual machine image. 
    __imagePath = ""
    
    ## ssh support.
    __sshExe = BashSshExecution()

    ## set ssh support on and off
    __isSSH = True

    def __init__(self):
        self.__sshExe.address = ""
        self.__sshExe.sshUser = "root"
        
    ## Set name of original virtual machine. For clone command.
    def setOriginalVM(self, name):
        self.__originalVM = name        
        
    ## Set home dir of owner.
    def setOwnersHome(self, name):
        name = name.replace(" ", "_")
        self.__ownersHome = name        
        
    ## Set name of Machine
    def setMachineName(self, name):
        name = name.replace(" ", "_")
        self.__vmName = name    
        
    ## Set RAM size.
    def setRAM(self, size):
        self.__ram = str(size)
        
    ## Set hard disc size.
    def setHdSize(self, size):   
        self.__hdSize = str(size)

    ## Set the path of ISO.
    def setIsoPath(self, path):        
        self.__IsoPath = path

    ## Create a new virual machine.
    def createNewMachine(self):
        self.__imagePath = self.__ownersHome + "/" + self.__vmName + ".img"
        _command =  "virt-install   --connect=qemu:///system "
        _command += " --force "
        _command += " --name " + self.__vmName 
        _command += " --ram " + self.__ram 
        _command += " --disk path=" + self.__imagePath + ","
        _command += "size=" + self.__hdSize + ","
        _command += "bus=virtio,"
        _command += "cache=writeback"
        _command += " --cdrom " + self.__IsoPath                                                            
        _command += " --accelerate "
        # set the divice of this network bridge...
#        _command += " --network bridge=externqabr0 "

        if self.__isSSH:
            __sshExe.do(_command)
        else:
            print "[Command]:",_command
            _f = subprocess.check_output(_command.split(),stderr=subprocess.STDOUT)
            _out = ""
            print "[_f]", _f
            for _line in _f:
                _out = _out + _line
            return  _out
        
    ## Clone a virtual machine....
    def cloneMachine(self):
        self.__imagePath = self.__ownersHome + "/" + self.__vmName + ".img"
        _command =  "virt-clone "
        _command += " --force "
        _command += " --original " + self.__originalVM
        _command += " --name " + self.__vmName 
        _command += " --file " + self.__imagePath
        
        if self.__isSSH:
            __sshExe.do(_command)
        else:        
            print "[Command]:",_command
            _f = subprocess.check_output(_command.split(),stderr=subprocess.STDOUT)
            _out = ""
            print "[_f]", _f
            for _line in _f:
                _out = _out + _line
            return  _out
        
    def getImagePath(self):
        return self.__imagePath