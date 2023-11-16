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
        lat = request.form.get("latitude")
        long = request.form.get("longitude")
        key2 = '1643b4cf13a64d90b17d34a4a8f2b3ff'
        KEY = '7d054aedbf7841b4b2154afb427cfd8b'
        rad = 1000
        url = f"https://api.geoapify.com/v2/places?categories=parking&filter=circle:{long},{lat},{rad}&bias=proximity:{long},{lat}&limit=10&apiKey={KEY}"

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
                places.append({"lat":lat,"lng":long,"address":place["formatted"]})

        return render_template("spots.html",locations=places)
    else:
        return redirect(url_for('main'))
        
@app.route("/route")
def route():
    long=13.0093
    lat=77.5741
    return redirect(f"http://maps.google.com/maps?z=12&t=m&q=loc:{long}+{lat}")

if __name__ == "__main__":
    app.run(debug=True)