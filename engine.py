import datetime
from datetime import datetime


import pandas as pd
import requests
import json


def get_data():
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

    date_format = "%Y-%m-%d %H:%M:%S"

    # Define a function to convert the datetime
    def convert_to_datetime(row):
        return datetime.strptime(row.replace('T', ' '), date_format)

    # Adding two columns for planned and actual time in datetime format
    df['planned_time'] = df['CHSTOL'].apply(convert_to_datetime)
    df['actual_time'] = df['CHPTOL'].apply(convert_to_datetime)

    df['delay'] = df['actual_time'] - df['planned_time']

    return df


def delays_depart():
    df = get_data()
    dfd = df.loc[(df['CHAORD'] == 'D') & (df['CHRMINE'] == 'DEPARTED')]

    average_delay_depart = dfd['delay'].mean()
    average_delay_by_airline = dfd.groupby(df['CHOPERD'])['delay'].mean()
    print('Average departure delay last 24 hours: ', average_delay_depart)
    print('departures: ', average_delay_by_airline.nlargest(5))
    print('departures: ', average_delay_by_airline.nsmallest(5)[::-1])


def delays_arrive():
    df = get_data()
    dfa = df.loc[(df['CHAORD'] == 'A') & (df['CHRMINE'] == 'LANDED')]

    average_delay_arrive = dfa['delay'].mean()
    average_delay_by_airline = dfa.groupby(df['CHOPERD'])['delay'].mean()
    print('Average arrival delay last 24 hours: ', average_delay_arrive)
    print('arrivals: ', average_delay_by_airline.nlargest(5))
    print('arrivals: ', average_delay_by_airline.nsmallest(5)[::-1])



