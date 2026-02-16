from flask import Flask, render_template, request
import requests
app = Flask(__name__)


import random
import requests

@app.route("/")
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



if __name__ == "__main__":
    app.run(debug=True)
