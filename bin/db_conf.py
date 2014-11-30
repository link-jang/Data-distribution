'''

@author: conny
'''

import MySQLdb
import configuration

global conn 
conn = None

def getConn():
    global conn
    if not conn :
        conf = configuration.getConf()
        conn = MySQLdb.connect(host=conf.get('db_host'), user = conf.get('db_user'),passwd= conf.get('db_passwd'), db= conf.get('db_database'), charset="utf8")  
        
    return conn

def getClientInfo():
    con = getConn()
    cursor = con.cursor()  
    sql = 'select distinct client_ip ,client_port from dir_metadata'
    cursor.execute(sql)
    clientInfo = []
    for row in cursor.fetchall(): 
        clientInfo.append(row )
    
    return clientInfo
    
    
def getDirInfo():
    con = getConn()
    cursor = con.cursor()  
    sql = 'select * from dir_task where notify = -1'
    cursor.execute(sql)
    dirInfo = []
    for row in cursor.fetchall(): 
        dirInfo.append(row )
    
    return dirInfo
    
    
def getRsyncStatus():
    con = getConn()
    cursor = con.cursor()  
    sql = 'select * from dir_task where notify > -1 and status = -1'
    cursor.execute(sql)
    dirInfo = []
    for row in cursor.fetchall(): 
        dirInfo.append(row )
    
    return dirInfo
    


    

if __name__ == '__main__':
   print  getDirInfo()
    
    
    