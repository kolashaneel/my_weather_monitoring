import logging
import logging.handlers
import os
import sys
import json
import configparser

from splunk.persistconn.application import PersistentServerConnectionApplication

sys.path.append('/opt/splunk/etc/apps/my_weather_monitoring/bin')
from security_1 import encrypt

def setup_logger(level):
    logger = logging.getLogger("custom_rest")
    logger.propagate = False
    logger.setLevel(level)
    log_file_path = os.environ['SPLUNK_HOME'] + '/var/log/splunk/custom_rest_handler.log'
    file_handler  = logging.handlers.RotatingFileHandler(log_file_path,maxBytes=2500000,backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger=setup_logger(logging.INFO)
cp=configparser.ConfigParser()
SPLUNK_HOME=os.environ['SPLUNK_HOME']
apps_path=os.path.join(SPLUNK_HOME,'etc','apps')
app_name="my_weather_monitoring"
local_path=os.path.join(apps_path,app_name,'local')
config_file_path=os.path.join(local_path,'configurations.conf')

class custom_handler(PersistentServerConnectionApplication):
    def __init__(self,command_line,command_arg):
        PersistentServerConnectionApplication.__init__(self)
    
    def handle(self, in_string):
        logger.info(in_string)
        payload = json.loads(in_string)

        def update_api_token(payload):
            if payload['form'][0][1]:
                api_token=str(payload['form'][0][1])
                encrypted_api_token=encrypt(api_token)
            else:
                api_token=""
            cp.read(config_file_path)
            cp["api_details"]["api_token"]=encrypted_api_token
            with open(config_file_path,'w') as file:
                cp.write(file)

        if payload['method']=="POST":
            update_api_token(payload)
            response="API Token Updated Successfully"
        else:
            response=f"this is a {payload['method']} request, this api supports only post method"

        return {'payload':f'{response}',
                'status':200}
    
    