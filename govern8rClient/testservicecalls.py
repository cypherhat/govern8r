import requests

r=requests.get('http://127.0.0.1:5000/govern8r/api/v1/pubkey')
data = r.json()
print data['public_key']
