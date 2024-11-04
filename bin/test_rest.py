import requests

response = requests.post("https://localhost:8089/services/resthandler",auth=('admin','splunk@123'),data={"a":"c3b6c5fde7f6336b0b7dc9005fcceb8e"},verify=False)

print(response.text,response.status_code)
