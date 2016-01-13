import requests

response = requests.get('https://127.0.0.1:5000/govern8r/api/v1/account/19sbnNShA5mQML6Xyia5HBrDEYycv7yTVa/b9ec8a84b7481e4e',verify=False)
print(response.status_code)