import requests
import json

TOKEN = ''
url = "https://trefle.io/api/species?token=" + TOKEN + "&q=sunflower"
response = requests.get(url)
json_data = json.loads(response.text)
print(json.dumps(json_data, indent=2))
print(json_data[0]['id'])

for item in json_data:
    url = "https://trefle.io/api/plants/" + str(item['id']) + "?token=" + TOKEN
    response = requests.get(url)
    plant_json_data = json.loads(response.text)
    print(plant_json_data['images'])
    if plant_json_data.get('images'):
        if len(plant_json_data['images']) > 0:
            print('found')
            print(plant_json_data['images'][0]['url'])
            print(item['id'])
            break
