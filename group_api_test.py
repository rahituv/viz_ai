import requests

my_keys = ["b3bebfe16ba241c4859e7c1277930842", "125091db2fb544d5b133e27d8c6808cd"]


headers = {'Content-Type': 'application/octet-stream',
           'Ocp-Apim-Subscription-Key': my_keys[0]}

face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
data = open('images/a.jpg', 'rb')
response = requests.post(face_api_url, headers=headers, data=data)
faces = response.json()
print faces