'''

@author: conny
'''

import httplib
import urllib


class HeartBeat(object):
    '''
    classdocs
    '''


    def __init__(self, host, port):
        '''
        Constructor
        '''
        self.host = host
        self.port = port
        
    
    def run(self):
    
        httpClient = None
     
        try:
            httpClient = httplib.HTTPConnection(self.host, self.port, timeout=5)
            httpClient.request('GET', '/heartbeat')
         
            response = httpClient.getresponse()
    
            return response.status, response.read()
        except Exception, e:
            return 404,'error'
            print e
        finally:
            if httpClient:
                httpClient.close()
                
                
                
                
class NotifyJob(object):
    '''
    classdocs
    '''


    def __init__(self, host, port, file_id, shell, param):
        '''
        Constructor
        '''
        
        self.host = host
        self.port = port
        self.file_id =file_id
        self.shell = shell
        self.param = param
        
        
    def run(self, ):
        
        httpClient = None
     
        try:
            params = urllib.urlencode({'id': self.file_id, 'shell': self.shell, 'param': self.param})
            headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}
            httpClient = httplib.HTTPConnection(self.host, self.port, timeout=5)
            
            
            httpClient.request('POST', '/runjob', params, headers)
         
            response = httpClient.getresponse()
    
            return response.status, response.read()
        except Exception, e:
            return 404,'error'
            print e
        finally:
            if httpClient:
                httpClient.close()
                
                
class CheckStatus(object):
    '''
    classdocs
    '''


    def __init__(self, host, port, file_id, shell, param):
        '''
        Constructor
        '''
        
        self.host = host
        self.port = port
        self.file_id =file_id
        self.shell = shell
        self.param = param
        
                
    def run(self):
        
        httpClient = None
     
        try:
            httpClient = httplib.HTTPConnection(self.host, self.port, timeout=5)
            httpClient.request('GET', '/checkstatus&id=' + str(self.file_id) + '&filename=' + str(self.filename) )
         
            response = httpClient.getresponse()
    
            return response.status, response.read()
        except Exception, e:
            return 404,'error'
            print e
        finally:
            if httpClient:
                httpClient.close()
                
                    
    
        