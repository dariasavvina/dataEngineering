import requests
import pandas as pd


response = requests.get('https://api.jsoning.com/mock/public/products')
response_json = response.json()

df = pd.DataFrame(response_json)
html_str = df.to_html('sixth_task_result.html', index=False)




