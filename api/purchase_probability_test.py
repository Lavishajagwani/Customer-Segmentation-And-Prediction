import requests

url = "http://127.0.0.1:5000/purchase-probability"
data = {
    "Age": 19,
    "Previous Purchases": 2,
    "Purchase Amount (USD)": 64,
    "Review Rating": 3.1
}


response = requests.post(url, json=data)
print(response.json())  # Expected Output: {"Purchase Probability": 1}
