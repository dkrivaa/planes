import datetime
from datetime import datetime


import pandas as pd
import requests
import json




url = "https://data.gov.il/api/3/action/datastore_search?resource_id=e83f763b-b7d7-479e-b172-ae981ddc6de5"

response = requests.get(url)

if response.status_code == 200:
    info = json.loads(response.text)
    url = 'https://data.gov.il/api/3/action/datastore_search'
    resource_id = info['result']['resource_id']
    # Extract the count of records
    count = info["result"]["total"]
    # Initialize an empty list to store the results
    results = []

    # Make multiple requests to retrieve all the rows
    for offset in range(0, count, count):
        params = {'resource_id': resource_id, 'limit': count, 'offset': offset}
        response = requests.get(url, params=params).json()
        data = response['result']['records']
        results.extend(data)

df = pd.DataFrame(results)




print(df.columns)
print(len(df))





