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

## The main window of the GUI
class VMinfoDB():

    ## Connection object that represents the database.
    ## Here the data will be stored in the /tmp/isar.db file
    __conn = sqlite3.connect('/tmp/isar.db')

    ## A Cursor object call its execute() method to perform SQL commands.
    __cursor = __conn.cursor()


    ## Constructor
    def __init__(self, *args):
        logging.debug('init main VMinfoDB....')
    

    def initDB(self):

        # Create table
        __conn.execute("create table vmachine ( \
            owner TEXT\
            name TEXT\
            create TEXT\
            best_befor TEXT\
            OS TEXT\
            ")

