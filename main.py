from flask import Flask, render_template, redirect, url_for, request
import requests
from requests.structures import CaseInsensitiveDict
from opencage.geocoder import OpenCageGeocode





app = Flask(__name__)

@app.route("/")
def main():
    return render_template("landing.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/spots",methods=["GET","POST"])
def spots():
    if request.method == "POST":
        lat = float(request.form.get("latitude"))
        long = float(request.form.get("longitude"))
        key2 = '1643b4cf13a64d90b17d34a4a8f2b3ff'
        KEY = '7d054aedbf7841b4b2154afb427cfd8b'
        rad = 750
        print(request.form)
        d = request.form.get("disabled")
        if d:
            url = f"https://api.geoapify.com/v2/places?categories=parking&conditions=wheelchair.yes&filter=circle:{long},{lat},{rad}&bias=proximity:{long},{lat}&limit=10&apiKey={KEY}"
        else:
            url = f"https://api.geoapify.com/v2/places?categories=parking&filter=circle:{long},{lat},{rad}&bias=proximity:{long},{lat}&limit=10&apiKey={KEY}"

        print(rad)
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        resp = requests.get(url, headers=headers)
        Response = eval(resp.text)


        url = f"https://api.geoapify.com/v2/places?categories=parking&conditions=wheelchair.yes&filter=circle:{long},{lat},{rad + 1000}&bias=proximity:{long},{lat}&limit=10&apiKey={KEY}"

        url1 = f"https://api.geoapify.com/v2/places?categories=parking&filter=circle:{long},{lat},{rad}&bias=proximity:{long},{lat}&limit=10&apiKey={KEY}"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        resp = requests.get(url, headers=headers)
        Response = eval(resp.text)
        
        d_places = []

        for item in Response["features"]:
            lat = item["properties"]["lat"]
            lon = item["properties"]["lon"]
            gc = OpenCageGeocode(key2)


            for place in gc.reverse_geocode(lat,lon):
                d_places.append({"lat":lat,"lng":long,"address":place["formatted"],"url":f"http://maps.google.com/maps?z=12&t=m&q=loc:{lat}+{long}"})

        places = []
        resp1 = requests.get(url1,headers=headers)
        Response1 = eval(resp1.text)

        for item in Response1["features"]:
            lat = item["properties"]["lat"]
            lon = item["properties"]["lon"]
            gc = OpenCageGeocode(key2)


            for place in gc.reverse_geocode(lat,lon):
                places.append({"lat":lat,"lng":long,"address":place["formatted"],"url":f"http://maps.google.com/maps?z=12&t=m&q=loc:{lat}+{long}"})


        return render_template("spots.html",dlocations=d_places,locations = places)
    else:
        return redirect(url_for('main'))
        
@app.route('/auto')
def auto():
    return render_template('auto.html')

@app.route('/sel')
def sel():
    return render_template("sel2.html")


if __name__ == "__main__":
    app.run()