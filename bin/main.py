'''

@author: conny
'''

from Timer import Timer
import job_fun



def heartbeatTask():
    
    checkdirTimer = Timer(1, 120, job_fun.checkOrgiDataAction)
    checkdirTimer.start()
    
    checkStatusTimer = Timer(1, 120, job_fun.checkSatusAction)
    checkStatusTimer.start()
 
    hearbeatTimer = Timer(1, 60, job_fun.heartBeatAction)
    hearbeatTimer.setDaemon(True)
    hearbeatTimer.start()
    
    
    

   



if __name__ == '__main__':
     heartbeatTask()