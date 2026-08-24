import requests
url = 'http://127.0.0.1:8000/items/6602615442?q=Chanyapak'
conn = requests.get(url)
print(conn.status_code)
