import requests

response = requests.get('http://127.0.0.1:5000/govern8r/api/v1/account/1KhiuzumwU1YkyBRZGKKecxgrQUuCZaLyb/8307a939616bfa4d')
print(response.status_code)