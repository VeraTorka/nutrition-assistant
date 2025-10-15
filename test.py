import pandas as pd

import requests

url = "http://localhost:5000/question"

question ="What is the vitamin C content in a 100g apple compared to an orange?"

data = {"question": question}

response = requests.post(url, json=data)
print(response.json())

