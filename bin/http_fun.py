'''

@author: conny
'''

import httplib

    

def HeartBeat(args = []):
    
    httpClient = None
 
    try:
        httpClient = httplib.HTTPConnection(args[0], args[1], timeout=5)
        httpClient.request('GET', '/heartbeat')
     

        response = httpClient.getresponse()

        return response.status, response.read()
    except Exception, e:
        return 404,'error'
        print e
    finally:
        if httpClient:
            httpClient.close()
            
            



if __name__ == '__main__':
    sts,content =  HeartBeat(['http://www.baidu.com','80'])
    print sts
    print content
    
    url = 'www.baidu.com?sdfb=30&'
    print len(url)
    if url[len(url) - 1] == '&':
        url = url[0: len(url) -2]
    print url
    
    