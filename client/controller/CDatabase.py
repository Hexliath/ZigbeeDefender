#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.MDatabase import *
import mysql.connector 
from utils.Config import *
import pandas as pd

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
            self.conn = mysql.connector.connect(
                host=self.db.db["host"],
                user=self.db.db["user"],
                passwd=self.db.db["password"],
                )
        except mysql.connector.errors.InterfaceError as e:
            print("SQL Database ({}) offline.".format(self.db.db["host"]))
            exit()

        self.cursor = self.conn.cursor()
        self.create() 


    def close(self):
        self.conn.close()
    
    def select(self,query):
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def pd_select(self,query):
        return pd.read_sql(query, self.conn)

        
    def insert(self,query,insert_tuple):
        self.cursor = self.conn.cursor(prepared=True)
     
        result  = self.cursor.execute(query, insert_tuple)
        self.conn.commit()

    def create(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self.db.db["db"]))
        self.cursor.execute("USE {}".format(self.db.db['db']))

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inputs (
            id int(10) NOT NULL AUTO_INCREMENT,
            original TEXT NOT NULL,
            device INTEGER NOT NULL,
            value FLOAT NOT NULL,
            sensor INTEGER NOT NULL,
            hours INTEGER NOT NULL,
            minutes INTEGER NOT NULL,
            day INTEGER NOT NULL,
            month INTEGER NOT NULL,
            PRIMARY KEY(id)
        );
        """)






