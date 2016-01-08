import requests

url = "http://127.0.0.1:5000/govern8r/api/v1/upload"
files = {'files': open('/Users/tssbk40/test.txt', 'rb')}
r = requests.post(url, files=files)
print r.status_code