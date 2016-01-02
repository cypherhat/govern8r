import requests

response = requests.get('http://127.0.0.1:5000/govern8r/api/v1/account/1FeCnu4QCEWepMJQ3abEVBDhMEGVLXVzCg/5f4df75f3a5792c2')
print(response.status_code)