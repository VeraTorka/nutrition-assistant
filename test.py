import pandas as pd

import requests

url = "http://localhost:5000/question"

question ="How much protein is in 100g of tofu?"

data = {"question": question}

response = requests.post(url, json=data)
print(response.json())

