from flask import Flask, render_template, redirect, url_for, request



long = 0
lat = 0




app = Flask(__name__)

@app.route("/")
def main():

    return render_template("landing.html")


@app.route('/test')
def test():
    return render_template("test.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/spots",methods=["GET","POST"])
def spots():
    if request.method == "POST":
        lat = request.form.get("latitude")
        long = request.form.get("longitude")

        parking = {
            [""]
        }

    else:
        return "EHH No location provided"

if __name__ == "__main__":
    app.run(debug=True)