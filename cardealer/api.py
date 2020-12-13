import urllib.request, urllib.parse, urllib.error
import json

print("Enter registration:")
registration=input

ApiUrl = "http://api.nrpla.de/"
url = ApiUrl + registration() +"?api_token=iZ3T9knspElwMyglvXbFKaKXK8co5k0LKjLzke6Uirnaw5FuqtE20SXKI4ttrZIM&advanced=1"

print('Retrieving', url)
uh = urllib.request.urlopen(url)
data = uh.read().decode()

js=json.loads(data)
brand = js["data"]["brand"]
model = js["data"]["model"]
engine = js["data"]['version']

print("Brand:", brand)
print("Model:", model)
print("Engine:", engine)