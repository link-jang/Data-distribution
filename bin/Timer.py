'''

@author: conny
'''

import threading
import time
import util

class Timer(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, num, interval, doAction, args = []):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.num = num 
        self.interval = interval
        self.doActin = doAction 
        self.args = args
        self.is_stop =  False 
        
    def run(self):
        
        while not self.is_stop:
            
            self.doActin(self.args)
            time.sleep(self.interval)
            





if __name__ == '__main__':
    list1 = ['/home/conny/a.sh', 'aa', 'cc']





