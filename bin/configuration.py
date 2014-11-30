'''

@author: conny
'''

import ConfigParser

global conf_data
conf_data = None

config = ConfigParser.ConfigParser()
config.read('../conf/config.conf')




def getConf():
    global conf_data
    if not conf_data:
        db_host = config.get('mysql','db_host')
        db_port = config.get('mysql','db_port')
        db_user = config.get('mysql','db_user')
        db_passwd = config.get('mysql','db_passwd')
        db_database = config.get('mysql','db_database')
        conf_data = {}
        conf_data['db_host'] = db_host
        conf_data['db_port'] = db_port
        conf_data['db_user'] = db_user
        conf_data['db_passwd'] = db_passwd
        conf_data['db_database'] = db_database
        
        return conf_data


if __name__ == '__main__':
    pass