import requests

url = "http://127.0.0.1:5000/segment"
data = {
    "Age": 26,
    "Purchase Amount (USD)": 97,
}



response = requests.post(url, json=data)
print(response.json())  # Expected Output: {"Customer Segment": 2}
