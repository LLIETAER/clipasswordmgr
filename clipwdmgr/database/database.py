#The MIT License (MIT)
#
#Copyright (c) 2015,2018 Sami Salkosuo
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

#database functions
import sqlite3
import os
from random import randint

from ..crypto.crypto import *
from ..utils.utils import *
from ..globals import *
from ..globals import GlobalVariables
from ..utils.settings import Settings

#sqlite database
DATABASE=None
#sqlite database cursor
DATABASE_CURSOR=None

#class Database():
def openDatabase():
    global DATABASE
    global DATABASE_CURSOR
    DATABASE=sqlite3.connect(':memory:')
    DATABASE.row_factory = sqlite3.Row
    DATABASE_CURSOR=DATABASE.cursor()
    sql=[]
    sql.append("CREATE TABLE accounts ")
    sql.append("(")
    for column in DATABASE_ACCOUNTS_TABLE_COLUMNS:
        sql.append(" ")
        sql.append(column)
        if column in DATABASE_ACCOUNTS_TABLE_COLUMN_IS_INTEGER:
            sql.append(" INTEGER ")
        else:
            sql.append(" TEXT ")
        if column in DATABASE_ACCOUNTS_TABLE_COLUMN_IS_TIMESTAMP:
            sql.append(" DEFAULT CURRENT_TIMESTAMP ")
        else:
            if column in DATABASE_ACCOUNTS_TABLE_COLUMN_IS_INTEGER:
                sql.append(" DEFAULT 0 ")
            else:
                sql.append(" DEFAULT '' ")
        sql.append(",")
    sql=sql[:-1]
    sql.append(")")
    sql="".join(sql)
    debug("Create SQL: %s " %sql)
    DATABASE_CURSOR.execute(sql)

def closeDatabase():
    global DATABASE
    global DATABASE_CURSOR
    if DATABASE is not None:
        DATABASE.close()
    DATABASE=None
    DATABASE_CURSOR=None

def executeSelect(listOfColumnNames,whereNameStartsWith=None,whereClause=None,orderBy=COLUMN_NAME,returnSQLOnly=False,useID=False):
    where=""
    if whereNameStartsWith is not None:
        if useID==False:
            where="where name like \"%s%%\"" % whereNameStartsWith
        else:
            where="where id = %s" % whereNameStartsWith
            
    if whereClause is not None:
        where=whereClause
    cols=",".join(listOfColumnNames)
    orderClause=""
    if orderBy is not None:
        orderClause="order by %s" % orderBy
    sql="select %s from accounts %s %s" % (cols,where,orderClause)
    debug("executeSelect SQL: %s" % sql)
    if returnSQLOnly==True:
        return sql
    else:
        return DATABASE_CURSOR.execute(sql)

def executeSql(sql,params=None,commit=False):
    if params!=None:
        rows=DATABASE_CURSOR.execute(sql,params)
    else:
        rows=DATABASE_CURSOR.execute(sql)
    if commit==True:
        DATABASE.commit()
    columns=DATABASE_CURSOR.description
    return (rows,columns)


def executeDelete(sql,params):
    DATABASE_CURSOR.execute(sql,params)
    DATABASE.commit()

def selectFirst(sql):
    #select and return first column and first row of sql result
    return (DATABASE_CURSOR.execute(sql).fetchone()[0])

def insertAccountToDB(accountString):
    accountDict=accountStringToDict(accountString)
    columnNames=[]
    values=[]
    qmarks=[]
    for key in accountDict.keys():
        value=accountDict[key]
        if value != "":
            columnNames.append(key)
            values.append(value)
            qmarks.append("?")
    sql=[]

    sql.append("insert into accounts (")
    sql.append(",".join(columnNames))
    sql.append(") values (")
    sql.append(",".join(qmarks))
    sql.append(")")
    sql="".join(sql)
    #debug("SQL: %s" % sql)
    #debug(tuple(values))
    DATABASE_CURSOR.execute(sql,values)

def insertAccountToFile(encryptionKey,accountString):
    encryptedAccount=encryptString(encryptionKey,accountString)
    appendStringToFile(GlobalVariables.CLI_PASSWORD_FILE,encryptedAccount)

#import accounts to database
#return False if no account file
def loadAccounts(encryptionKey=None,cmd=None):

    if encryptionKey==None:
        encryptionKey=GlobalVariables.KEY

    if os.path.isfile(GlobalVariables.CLI_PASSWORD_FILE) == False:
        if cmd != "add":
            print("No accounts. Add accounts using add-command.")
        return False

    accounts=readFileAsList(GlobalVariables.CLI_PASSWORD_FILE)
    for account in accounts:
        if account==None or account=="":
            continue
        decryptedAccount=decryptString(encryptionKey,account)
        insertAccountToDB(decryptedAccount)

    return True

def accountStringToDict(str):
    account=str.split(FIELD_DELIM)
    accountDict=dict()
    for field in account:
        ind=field.find(":")
        name=field[0:ind]
        value=field[ind+1:]
        accountDict[name]=value
        #print("%s == %s" % (name,value))
    return accountDict

def generateNewID():
    newId=0
    settingsObj=Settings()
    while newId==0:
        newId=randint(1, int(settingsObj.get(SETTING_MAX_ID)))
        rows=executeSelect([COLUMN_ID],whereClause="where %s = %d" % (COLUMN_ID,newId) )
        #print(rows)
        for row in rows:
            if row[COLUMN_ID] == None:
                newId=0
    return newId
            
