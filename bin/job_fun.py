'''

@author: conny
'''

import os
import db_obj
import http_rpc
import threading,time
import util


class BashThread(threading.Thread):
    
    def __init__(self, cmd, timeout,beforeAction = None,beforParam=None, afterAction = None, afterParam=None):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout
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
            pass
            
            
        if self.afterAction:
            if self.afterParam:
                self.afterAction(self.afterParam)
            else:
                self.afterAction()
    

def  checkOrgiDataAction():
    dbObj = db_obj.getDbObj()
    dirInfo = dbObj.getDirInfo()
    
    for dir in dirInfo:
        task_id,file_id,filename,server_shell,server_param,client_ip,client_port,client_shell,client_param,day,hour = dir
        
        if os.path.exists(filename):
            bashbase = []
            bashbase.append(server_shell)
            bashbase.extend(str(server_param).split(' '))
            exeBash = BashThread(bashbase,3600,beforeAction=dbObj.beforRsync, beforParam=file_id,
                                        afterAction = dbObj.beforRsync)
        else:
            pass
            

        
def heartBeatAction():
    dbObj = db_obj.getDbObj()
    clientInfo = dbObj.getClientInfo()
    for client in  clientInfo:
        heartBeatObj = http_rpc.HeartBeat(client[0], client[1])
        sts , text = heartBeatObj.run()
        print (client[0], client[1], sts, text)



if __name__ == '__main__':
    print heartBeatAction()