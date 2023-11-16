import requests
from requests.structures import CaseInsensitiveDict
from opencage.geocoder import OpenCageGeocode

def GetParking(lat, long, rad):
        

    key2 = '1643b4cf13a64d90b17d34a4a8f2b3ff'
    KEY = '7d054aedbf7841b4b2154afb427cfd8b'

    url = f"https://api.geoapify.com/v2/places?categories=parking&filter=circle:{long},{lat},{rad}&bias=proximity:{long},{lat}&limit=1&apiKey={KEY}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)
    Response = eval(resp.text)


    places = []

    for item in Response["features"]:
        lat = item["properties"]["lat"]
        lon = item["properties"]["lon"]
        gc = OpenCageGeocode(key2)


        for place in gc.reverse_geocode(lat,lon):
            print(place["formatted"])
            places.append({"lat":lat,"long":lon,"address":place["formatted"]})

    return (lat, lon)