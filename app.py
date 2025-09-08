from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "הכל תקין ב־Flixbaba API!",
        "status": "online"
    })

@app.route('/movies')
def get_movies():
    url = "https://flixbaba.tv"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, "html.parser")

        movies = []

        # בדיקה לפי מה שראינו בקוד: תמונות של הסרטים
        for item in soup.select("a.MuiBox-root img"):  # CSS class מהאתר
            parent = item.find_parent("a")
            if parent:
                movies.append({
                    "title": item.get("alt"),
                    "image": item.get("src"),
                    "link": "https://flixbaba.tv" + parent.get("href")
                })

        return jsonify(movies)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
