import requests

url = "http://localhost:8000/bmi"

patient = {
    "name": "Anjali Patil",
    "weight_kg": 55,
    "height_cm": 158
}

response = requests.post(url, json=patient)

print(response.json())