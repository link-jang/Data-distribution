'''

@author: conny
'''
import MySQLdb
import time


global db_obj
db_obj = None
import configuration

class DbObj(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.conn = self.getConn()
        
    def getConn(self):
        conf = configuration.getConf()
        conn = MySQLdb.connect(host=conf.get('db_host'), user = conf.get('db_user'),passwd= conf.get('db_passwd'), db= conf.get('db_database'), charset="utf8")      
        return conn
    
    def getClientInfo(self):

        cursor = self.conn.cursor()  
        sql = 'select distinct client_ip ,client_port from dir_metadata'
        cursor.execute(sql)
        clientInfo = []
        for row in cursor.fetchall(): 
            clientInfo.append(row )
        cursor.close()
        return clientInfo
    
    def beforRsync(self, file_id):
        cursor = self.conn.cursor()  
        sql = 'update dir_task set exist =-2 where file_id = %s'
        param = (file_id)
        cursor.execute(sql, param)
        self.conn.commit()
        
    def afterRsync(self,file_id, exits =None, notify=None):
        cursor = self.conn.cursor()  
        sql = 'update dir_task set exist =%s , notify =%s where file_id = %s'
        param = (exits, notify)
        cursor.execute(sql, param)
        self.conn.commit()
        
    def getDirInfo(self):

        cursor = self.conn.cursor()  
        sql = 'select task_id,file_id,filename,server_shell,server_param,client_ip,client_port,client_shell,client_param,day,hour from dir_task where exist = -1'
        cursor.execute(sql)
        dirInfo = []
        for row in cursor.fetchall(): 
            dirInfo.append(row )
        cursor.close()
        return dirInfo
        
        
    def getRsyncStatus(self):

        cursor = self.conn.cursor()  
        sql = 'select file_id,client_ip,client_port from dir_task where notify > -1 and status = -1'
        cursor.execute(sql)
        fileInfo = []
        for row in cursor.fetchall(): 
            fileInfo.append(row )
        cursor.close()
        return fileInfo
    
    def upateStatus(self, file_id, status):

        cursor = self.conn.cursor()  
        sql = 'upate dir_task set status = %s where file_id=%s  and status = -1'
        param = (file_id, status)
        cursor.execute(sql, param)
        cursor.close()
        self.conn.commit() 
        
        
    def checkHourJob(self, day, hour):
        cursor = self.conn.cursor()
        sql = 'select count(file_id) from dir_task  where  day=%s and hour=%s'
        param = (day, hour)
        cursor.execute(sql, param)
        task_count = 0
        for row in cursor.fetchall(): 
            task_count = row[0]
        
        sql = 'select count(*) from dir_metadata where cacul_period="hour" '
        cursor.execute(sql)
        meta_count = 0
        for row in cursor.fetchall(): 
            meta_count = row[0]
            
        if task_count == meta_count:
            return True
        else :
            return False
        
    def checkDayJob(self, day):
        cursor = self.conn.cursor()
        sql = 'select count(file_id) from dir_task  where  day=%s and hour=-1'
        param = (day)
        cursor.execute(sql, param)
        task_count = 0
        for row in cursor.fetchall(): 
            task_count = row[0]
        
        sql = 'select count(*) from dir_metadata where cacul_period=%s '
        param = ('day')
        cursor.execute(sql, param)
        meta_count = 0
        for row in cursor.fetchall(): 
            meta_count = row[0]
            
        if task_count == meta_count:
            return True
        else :
            return False
        
        
    def ceateJob(self):
        
        day = time.strftime('%Y%m%d',time.localtime(time.time()))
        hour = time.strftime('%H',time.localtime(time.time()))
        
        cursor = self.conn.cursor()
        
        #hour
        if not self.checkHourJob(day, hour):
            sql = ' select file_id, filereg, client_ip, client_port, client_shell, client_param from dir_metadata where cacul_period ="hour" '
            cursor.execute(sql)
            for row in cursor.fetchall(): 
                file_id, filereg, client_ip, client_port, client_shell, client_param = row 
                filereg = str(filereg).replace('${day}', day).replace("${hour}", hour)
                
                insert_sql = 'insert into dir_task(file_id, filename, client_ip, client_port, client_shell, client_param, day, hour) values(%s, %s, %s, %s, %s, %s, %s, %s)'
                param = (file_id, filereg, client_ip, client_port, client_shell, client_param, day, hour)
                sts = cursor.execute(insert_sql, param)
                if sts != 1:
                    return False
                
        #day
        if not self.checkDayJob(day):
            sql = ' select file_id, filereg, client_ip, client_port, client_shell, client_param from dir_metadata where cacul_period ="day" '
            cursor.execute(sql)
            for row in cursor.fetchall(): 
                file_id, filereg, client_ip, client_port, client_shell, client_param = row 
                filereg = str(filereg).replace('${day}', day)
                
                insert_sql = 'insert into dir_task(file_id, filename, client_ip, client_port, client_shell, client_param, day, hour) values(%s, %s, %s, %s, %s, %s, %s, -1)'
                param = (file_id, filereg, client_ip, client_port, client_shell, client_param, day)
                sts = cursor.execute(insert_sql, param)
                if sts != 1:
                    return False    
                
        cursor.close()
        self.conn.commit() 
    
def getDbObj():
    global db_obj
    if not db_obj:
        db_obj = DbObj()
    return db_obj


if __name__ == '__main__':
    obj = getDbObj()
    obj.ceateJob()

#     print time.strftime('%H',time.localtime(time.time()))


    