
import requests

endpoint = "http://localhost:8000/api/products/1/"
data = {
    "title": ";lkasjd;lfkasjd",
    "content": ";laksdjf",
    "price": 233.33
}
get_response = requests.get(endpoint)
print(get_response.json())