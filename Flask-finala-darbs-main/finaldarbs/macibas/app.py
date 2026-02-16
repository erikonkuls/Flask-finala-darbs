from flask import Flask, render_template, request, redirect
import sqlite3
import requests
app = Flask(__name__)


import random
import requests

@app.route("/sakumlapa")
def home():
    quote = "No quote available"

    try:
        response = requests.get(
            "https://api.npoint.io/970cafd42b7e63342718",timeout=5)
        response.raise_for_status()

        data = response.json()
        if isinstance(data, dict):
            quotes = data.get("quotes", [])
            if quotes:
                quote = random.choice(quotes)["text"]

    except requests.RequestException as e:
        app.logger.error(f"Error fetching quote: {e}")
        quote = "Could not fetch quote"

    return render_template("sakumlapa.html", quote=quote)



@app.route("/fizika")
def fizika():
    return render_template("fizika.html")

@app.route("/fizika2")
def fizika2():
    return render_template("fizika2.html")

@app.route("/kimija")
def kimija():
    return render_template("kimija.html")

@app.route("/kimija2")
def kimija2():
    return render_template("kimija2.html")

@app.route("/biologija")
def biologija():
    return render_template("biologija.html")

@app.route("/biologija2")
def biologija2():
    return render_template("biologija2.html")

@app.route("/programesana2")
def programesana2():
    return render_template("programesana2.html")

@app.route("/angluval2")
def angluval2():
    return render_template("angluval2.html")

@app.route("/matematika")
def matematika():
    return render_template("matematika.html")

@app.route("/matematika2")
def matematika2():
    return render_template("matematika2.html")


@app.route("/login")
def loigin():
    return render_template("login.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")   

@app.route("/sakumlapa")
def sakumlapa():    
    return render_template("sakumlapa.html")


@app.route("/")
def pievienoties():
    return render_template("sakumlapa2.html")



@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("./database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return redirect("/sakumlapa")
        else:
            return redirect("/login")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        if name:
            conn = sqlite3.connect("./database.db")
            conn.execute("INSERT INTO users (name, surname, phone, email, password) VALUES (?, ?, ?, ?, ?)", (name, surname, phone, email, password))
            conn.commit()
            conn.close()
            return redirect("/sakumlapa")
    


     


if __name__ == "__main__":
    app.run(debug=True)




