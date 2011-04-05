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
from UserInfo import UserInfo


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
        
    ## Destructor.
    def __del__(self):
        self.__conn.close()
    
    ## Create table
    def initDB(self):

        # Create table
        self.__conn.execute('CREATE TABLE  vmachine( \
            id INTEGER PRIMARY KEY, \
            name TEXT NOT NULL, \
            createdate TEXT NOT NULL, \
            livetimedays TEXT NOT NULL, \
            comment TEXT NOT NULL, \
            mail TEXT NOT NULL, \
            image_file TEXT NOT NULL, \
            owner TEXT NOT NULL, \
            os TEXT NOT NULL );')

        # Create table
        self.__conn.execute('CREATE TABLE  user( \
            nickname TEXT PRIMARY KEY, \
            homedir TEXT NOT NULL, \
            mail TEXT NOT NULL, \
            fullname TEXT NOT NULL);')

        # Create table
        self.__conn.execute('CREATE TABLE  instaliso( \
            name TEXT PRIMARY KEY, \
            path TEXT NOT NULL);')
        self.__conn.commit()

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
            os \
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
        self.__conn.commit()

    ## add V-Machine info in database
    ## @param vminfo a VMinfo-class with info about V-Machine
    def addUser(self, nickname):
        print "[addUser...]"
        self.__conn.execute("insert into user( \
            nickname, \
            homedir, \
            mail, \
            fullname \
            ) values ( \
            '" + nickname + "', \
            '', \
            '', \
            '' \
            );")   
        self.__conn.commit()
        
        
    ## add install ISO path info in database
    ## @param name name of install ISO
    def addISOpath(self, name):
        print "[addISOpath...]"
        self.__conn.execute("insert into instaliso( \
            name, \
            path \
            ) values ( \
            '" + name + "', \
            '' \
            );")   
        self.__conn.commit()       
            
    ## @return get back a list of all user as UserInfo list.
    def getAllUser(self):
        userList = list()
        rows = self.__conn.execute("SELECT * FROM user")
        for row in rows:
            nickname, homedir, mail, fullname = row
            userInfo = UserInfo()
            userInfo.nickname = nickname
            userInfo.homedir = homedir
            userInfo.mail = mail
            userInfo.fullname = fullname
            userList.append(userInfo)
        return userList
        
         
    ## @return get back a list of all ISO names as strings.
    def getAllISOnames(self):
        nameList = list()
        rows = self.__conn.execute("SELECT name FROM instaliso")
        for row in rows:
            name = row
            userList.append(name)
        return userList  
        
         
    ## @return get back a path of a ISO as string.
    # @param name of ISO
    def getISOpath(self, name):
        _path = ""
        rows = self.__conn.execute("SELECT path FROM instaliso \
            WHERE name='" + name + "';")
        for row in rows:
            _path = row
        if  len(rows) < 1:
            return -1
        else:
            return _path      
        

    ## @param nickname A nickname of a user.
    # @return get back a user as UserInfo with set nickname.
    # if nickname not found in database, is retourn -1
    def getUser(self, nickname):
        userList = list()
        rows = self.__conn.execute("SELECT * FROM user WHERE nickname='" + nickname + "';")
        for row in rows:
            nickname, homedir, mail, fullname = row
            userInfo = UserInfo()
            userInfo.nickname = nickname
            userInfo.homedir = homedir
            userInfo.mail = mail
            userInfo.fullname = fullname
            userList.append(userInfo)
            
        if  len(userList) < 1:
            return -1
        else:
            return userList[0]
            
    ## Delete a user.
    def deleteUser(self, nickname):
        self.__conn.execute("DELETE FROM user \
            WHERE nickname = '" + nickname + "';") 
        self.__conn.commit()  

    ## Delete a user.
    def deleteISOpath(self, name):
        self.__conn.execute("DELETE FROM instaliso \
            WHERE name = '" + nickname + "';") 
        self.__conn.commit()  
        
    ## Update user data.   
    def updateUser(self, userInfo):
        _sql_string = "UPDATE user  SET \
            homedir = '" + userInfo.homedir + "', \
            mail = '" + userInfo.mail + "', \
            fullname = '" + userInfo.fullname + "' \
            WHERE nickname = '" + userInfo.nickname + "';"
        self.__conn.execute(_sql_string)
        self.__conn.commit()
                 
            