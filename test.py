#!/usr/bin/python3
#coding:utf-8

import sqlite3

conn =  sqlite3.connect("inform.db")
print("Opened database successfully")
c = conn.cursor()
c.execute('''CREATE TABLE LOG
       (articleId INT PRIMARY KEY     NOT NULL,
       articleTitle           TEXT    NOT NULL,
       downLink               TEXT    NOT NULL,
       ifDownloaded           BOOLEAN   NOT NULL);''')
print("Table created successfully")
c.execute("INSERT INTO LOG(articleId, articleTitle, downLink, ifDownloaded) VALUES(123455,'antenna','https',0)")
c.execute("INSERT INTO LOG(articleId, articleTitle, downLink, ifDownloaded) VALUES(123458,'antenna','https',0)")
c.execute("INSERT INTO LOG(articleId, articleTitle, downLink, ifDownloaded) VALUES(123459,'antenna','https',0)")

conn.commit()

cursor = c.execute("SELECT *from LOG WHERE articleId = 123455")
for row in cursor:
   print((row[0]))
   print( row[1])
   print( row[2])
   print( type(row[3]), "\n")

conn.close()  

