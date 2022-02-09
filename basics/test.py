import requests

url = "http://127.0.0.1:5000/store"

headers = {
       "Content-Type": "application/json"
}
data = {}
data["name"] = "Another Store"

response = requests.request("POST", url, headers=headers, json=data)

print(response.text)