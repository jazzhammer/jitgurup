import requests

# endpoint = "https://httpbin.org/status/200"
# endpoint = "https://httpbin.org/"
endpoint = "http://localhost:8000/api"

get_response = requests.post(
    endpoint,
    json={"product_id": 234, "title": "a;sdf"}
)
print(get_response.status_code)
print(get_response.json())

