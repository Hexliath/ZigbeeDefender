#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.MDatabase import *
#import mysql.connector 
import MySQLdb
from utils.Config import *

class CDatabase:
    db = None
    conn = None
    cursor = None

    def __init__(self):
        section = "mariadb"
        c = Config()
        self.db = MDatabase(
            c.get(section,"host"),
            c.get(section,"port"), 
            c.get(section,"db"),
            c.get(section,"user"),
            c.get(section,"password"))
        try:
            self.conn = MySQLdb.connect(
                host=self.db.db["host"],
                user=self.db.db["user"],
                passwd=self.db.db["password"],
                )
            
        except Exception as e:
            print("SQL Database ({}) offline.".format(self.db.db["host"]))
            exit()

        self.cursor = self.conn.cursor()
        self.create()

    def close(self):
        self.conn.close()
    
    def select(self,request):
        if(request.split(" ").upper() == "SELECT"):
            pass
    
    def insert(self,query):
        self.cursor = self.conn.cursor()
        result  = self.cursor.execute(query)
        self.conn.commit()

    def create(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self.db.db["db"]))
        self.cursor.execute("USE {}".format(self.db.db['db']))
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inputs (
            id int(10) NOT NULL AUTO_INCREMENT,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            pan_id TEXT NOT NULL,
            encryption INTEGER NOT NULL,
            radius TEXT NOT NULL,
            original TEXT NOT NULL,
            device INTEGER NOT NULL,
            zbee_counter INTEGER NOT NULL,
            frame_counter INTEGER NOT NULL,
            value FLOAT NOT NULL,
            sensor INTEGER NOT NULL,
            hours INTEGER NOT NULL,
            minutes INTEGER NOT NULL,
            day INTEGER NOT NULL,
            month INTEGER NOT NULL,
            result INTEGER NOT NULL,
            PRIMARY KEY(id)
        );
        """)
