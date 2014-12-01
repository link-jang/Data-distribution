'''

@author: conny
'''

import os
import db_obj
import http_rpc
import threading,time
import util


class BashThread(threading.Thread):
    
    def __init__(self, cmd, timeout,client_ip,client_port,file_id,client_shell,client_param,beforeAction = None,beforParam=None, afterAction = None, afterParam=None):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout
        self.client_ip = client_ip
        self.client_port = client_port
        self.file_id = file_id
        self.client_shell = client_shell
        self.client_param = client_param
        self.beforeAction = beforeAction
        self.beforParam = beforParam
        self.afterAction = afterAction
        self.afterParam = afterParam
        
    def run(self):
        if self.beforeAction:
            if self.beforParam:
                self.beforAction(self.beforParam)
            else:
                self.beforAction()
            
        sts,text =  util.command(self.cmd, self.timeout)
        
        notify = -1
        if sts == 0:
            notify = self.notify()
            
            
        if self.afterAction:
            if self.afterParam:
                self.afterAction(self.afterParam)
            else:
                self.afterAction((sts, notify))
                
    def notify(self):
        notifyobj = http_rpc.NotifyJob(self.client_ip, self.client_port,self.file_id, self.client_shell, self.param)
        sts, text = notifyobj.run()
        return stst
    
    
def checkOrgiDataAction():
    dbObj = db_obj.getDbObj()
    dirInfo = dbObj.getDirInfo()
    print 'checkdir'
    for dir in dirInfo:
        task_id,file_id,filename,server_shell,server_param,client_ip,client_port,client_shell,client_param,day,hour = dir
        
        if os.path.exists(filename):
            bashbase = []
            bashbase.append(server_shell)
            bashbase.extend(str(server_param).split(' '))
            exeBash = BashThread(bashbase,3600,client_ip,client_port, file_id,client_shell,client_param,beforeAction=dbObj.beforRsync, beforParam=file_id,
                      afterAction = dbObj.afterRsync)
            exeBash.start()
        else:
            pass
            

        
def heartBeatAction():
    dbObj = db_obj.getDbObj()
    clientInfo = dbObj.getClientInfo()
    for client in  clientInfo:
        heartBeatObj = http_rpc.HeartBeat(client[0], client[1])
        sts , text = heartBeatObj.run()
        print (client[0], client[1], sts, text)


def checkSatusAction():
    dbObj = db_obj.getDbObj()
    fileInfo = dbObj.getRsyncStatus()
    print 'check stats'
    for file in fileInfo:
        file_id, client_ip, client_port = file
        checkStatusObj = CheckStatus(client_ip, client_port, file_id)
        
        sts , text = checkStatusObj.run()
        dbObj = db_obj.getDbObj()
        dbObj.upateStatus(file_id, int(text))
        print (file_id, text)



if __name__ == '__main__':
    print checkOrgiDataAction()