import requests
import json
with open("insta_dump.json") as f:
	data = json.load(f)
for obj in data:
    r = requests.post('https://grocerybuddybackend.azurewebsites.net/item', json=obj)
    print(r.status_code)