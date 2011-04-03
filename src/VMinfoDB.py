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


import logging
import sqlite3


## @file VMinfoDB.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## The class manage the database operations
class VMinfoDB():

    dbPath = '/tmp/isar.db'

    ## Connection object that represents the database.
    ## Here the data will be stored in the /tmp/isar.db file
    __conn = sqlite3.connect(dbPath)

    ## A Cursor object call its execute() method to perform SQL commands.
    __cursor = __conn.cursor()


    ## Constructor
    def __init__(self):
        logging.debug('init main VMinfoDB....')
    
    ## Create table
    def initDB(self):

        # Create table
        self.__conn.execute('CREATE TABLE  vmachine( \
            id INTEGER PRIMARY KEY, \
            name TEXT, \
            createdate TEXT, \
            livetimedays TEXT, \
            comment TEXT, \
            mail TEXT, \
            image_file TEXT \
            owner TEXT, \
            OS TEXT );')

        # Create table
        self.__conn.execute('CREATE TABLE  user( \
            nickname TEXT PRIMARY KEY, \
            homedir TEXT, \
            mail TEXT, \
            fullname TEXT, \
            comment TEXT);')

        # Create table
        self.__conn.execute('CREATE TABLE  installiso( \
            name TEXT PRIMARY KEY, \
            path TEXT);')

    ## add V-Machine info in database
    ## @param vminfo a VMinfo-class with info about V-Machine
    def addVMinfo(self, vminfo):
        self.__conn.execute("insert into metatdata ( \
            name, \
            createdate, \
            livetimedays, \
            comment, \
            mail, \
            image_file, \
            owner, \
            OS \
            ) values ( \
            '" + vminfo.name + "', \
            '" + vminfo.createdate + "', \
            '" + vminfo.livetimedays + "', \
            '" + vminfo.comment + "', \
            '" + vminfo.mail + "', \
            '" + vminfo.image_file + "', \
            '" + vminfo.owner + "', \
            '" + vminfo.OS + "' \
            );")

            