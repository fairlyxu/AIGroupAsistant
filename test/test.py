import requests

url = "http://127.0.0.1:5001/generate"

payload = {
    "requestid": "8eaaaaadddssssdddd",
    "num": 7,
    "activaty_id": 1,
    "users": [1, 2, 3, 4]
}
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "PostmanRuntime-ApipostRuntime/1.1.0",
    "Connection": "keep-alive",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)