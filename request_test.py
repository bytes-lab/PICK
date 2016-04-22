import requests
import json

body = {
	"apiKey": "622a6564-6c73-4350-94f5-072a406fd4b7",
	"booking":{
		"pickupDetail": {
			"name": "Rupert",
			"phone": "1234567890",
			"address": "57 luscombe st, brunswick, melbourne"
		},
		"dropoffDetail": {
			"name": "Igor",
			"phone": "0987654321",
			"address": "105 collins st, 3000"
		}
	}
}            

req = requests.post(url='https://app.getswift.co/api/v2/quotes', headers={"Content-Type": "application/json"}, data=json.dumps(body))

print req.json()