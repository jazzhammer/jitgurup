import requests

endpoint = "http://localhost:8000/api/products/"
data = {
    "title": ";lkasjd;lfkasjd",
    "content": ";laksdjf",
    "price": 233.33
}
post_response = requests.post(endpoint, json=data)
print(post_response.json())