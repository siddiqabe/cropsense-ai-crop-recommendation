import requests
import json

# Data to send
data = {
    "N": 80,
    "P": 50,
    "K": 40,
    "temperature": 25,
    "humidity": 70,
    "ph": 6.5,
    "rainfall": 150
}

try:
    # Send POST request
    response = requests.post(
        "http://127.0.0.1:5000/predict",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    # Print response
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    
except requests.exceptions.ConnectionError:
    print("❌ Error: Cannot connect to Flask server. Make sure it's running on port 5000")
except Exception as e:
    print(f"❌ Error: {e}")