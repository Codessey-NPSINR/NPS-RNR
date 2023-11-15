from flask import Flask, render_template, redirect, url_for, request
import flask_login
from werkzeug.security import check_password_hash,generate_password_hash

long = 0
lat = 0




app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
        return render_template("landing.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)