import requests
import json
import os
import sys
import security_1
import configparser
import time
from extract_fields import extract_fields_from_json

SPLUNK_HOME = os.environ["SPLUNK_HOME"]
app_name = "my_weather_monitoring"
app_path=os.path.join(SPLUNK_HOME,'etc/apps',app_name)
configurations_path = os.path.join(SPLUNK_HOME,"etc/apps",app_name,'local','configurations.conf')
sys.path.append(os.path.join(app_path,'lib'))

from splunklib.searchcommands import dispatch,GeneratingCommand,Configuration,Option,validators

@Configuration()
class GetApiDetails(GeneratingCommand):
    api=Option(require=True)

    def call_api(self,api):
        cp = configparser.ConfigParser()
        cp.read(configurations_path)
        encrypted_api_token=cp["api_details"]["api_token"]
        decrypted_api_token=security_1.decrypt(encrypted_api_token)
        api=api+f"&appid={decrypted_api_token}"
        response=requests.get(api)
        response=response.text
        return response

    def generate(self):
        api_details=self.call_api(self.api)
        output_response={'_time':time.time(),'_raw':api_details}
        extracted_fields = extract_fields_from_json(json.loads(api_details))
        output_response.update(extracted_fields)
        yield output_response


dispatch(GetApiDetails,sys.argv,sys.stdin,sys.stdout,__name__)