import os
import sys
import base64

SPLUNK_HOME=os.environ['SPLUNK_HOME']
apps_path=os.path.join(SPLUNK_HOME,'etc','apps')
app_name="my_weather_monitoring"
lib_path=os.path.join(apps_path,app_name,'lib')
default_path=os.path.join(apps_path,app_name,'default')
public_key_path=os.path.join(default_path,'publickey.pub')
private_key_path=os.path.join(default_path,'privatekey.pem')

sys.path.append(lib_path)
import rsa

def readfile(file):
    with open(file,'r') as f:
        content = f.readlines()
        content="".join(content)
    return content

def encrypt(data):
    public_key=readfile(public_key_path)
    public_key = rsa.PublicKey.load_pkcs1(public_key.encode('utf-8'))
    data=data.encode('utf8')
    encrypted_data=rsa.encrypt(data,public_key)
    data = base64.b64encode(encrypted_data).decode('utf-8')
    return data

def decrypt(data):
    private_key=readfile(private_key_path)
    private_key = rsa.PrivateKey.load_pkcs1(private_key.encode('utf-8'))
    data=rsa.decrypt(base64.b64decode(data),private_key)
    data=data.decode('utf8')
    return data

# print(encrypt("shaneel"))
# print(decrypt("BERU1zqDMGbw0CNxKrZH2aOLrUmINcTerHIoFrh4RoMzSOlbGVjJT2o/SRq8UEy/TLDAJ5hQvPUt3JcKcbHKOSrPP4bNYpD3pdlJoPk3V8CZ1mbVDPQcYXxsl0zV2KsFh08AEBdDq50JAi2O5fCZLCPsHGxYSD2Qd7Gj6hSmEGYW"))

# print(encrypt("shaneel"))