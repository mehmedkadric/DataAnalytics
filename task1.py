import pandas as pd
from pandas import read_csv
import numpy as np
import os
from geopy import geocoders
from geopy.geocoders import GoogleV3


def loadDataset():
    business = pd.read_csv('businesses_plus.csv', encoding='latin-1')
    inspections = pd.read_csv('inspections_plus.csv', encoding='latin-1')
    violations = pd.read_csv('violations_plus.csv', encoding='latin-1')
    return business, inspections, violations


def newDatasets(ds):
    highQuality = []
    midQuality = []
    lowQuality = []
    return highQuality, midQuality, lowQuality


def classifier(business, inspections, violations, highQuality, midQuality, lowQuality):
    numberOfMissingValues = business.isnull().sum(axis=1)
    business = business.fillna(value="*")

    for i in range(len(business)):
        if business['name'].loc[i] != "*" and business['phone_number'].loc[i] != "*" and numberOfMissingValues[i] < 3:
            highQuality.append(business['business_id'].loc[i])
        else:
            if business['name'].loc[i] != "*" and numberOfMissingValues[i] < 4:
                midQuality.append(business['business_id'].loc[i])
            else:
                lowQuality.append(business['business_id'].loc[i])

    print(len(highQuality))
    print(len(midQuality))
    print(len(lowQuality))


def check(df):
    API_KEY = os.getenv("AIzaSyDLXOEyfx0Hu2hoft908Qg8pr3hCQhfTt8")
    g = GoogleV3(api_key=API_KEY)
    loc_lat = []
    loc_long = []
    loc_address = []
    for address in df.address:
        if address == 'nan':
            continue
        try:
            inputAddress = address
            location = g.geocode(inputAddress, timeout=15)
            loc_lat.append(location.latitude)
            loc_long.append(location.longitude)
            loc_address.append(inputAddress)
        except Exception as e:
            print('Error, skipping address...', e)
    df1 = pd.DataFrame(
        {'latitude': loc_lat,
         'longitude': loc_long
         })
    df1.to_csv('latitudeAndLongitude.csv')


if __name__ == "__main__":
    business, inspections, violations = loadDataset()
    highQuality, midQuality, lowQuality = newDatasets(business)
    classifier(business, inspections, violations, highQuality, midQuality, lowQuality)
