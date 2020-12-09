import requests

image_to_send = 'file.png'
url = "https://fastapitutorial.azurewebsites.net/predict"

image = open(image_to_send, "rb").read()
payload = {"file": image}

r = requests.post(url, files=payload).json()

print(r)
