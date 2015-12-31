import requests

response = requests.get('http://127.0.0.1:5000/govern8r/api/v1/account/1KhiuzumwU1YkyBRZGKKecxgrQUuCZaLyb/bee84938bb1ff5fe')
print(response.status_code)