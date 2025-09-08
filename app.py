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
    url = "https://flixbaba.app"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        movies = []
        movie_items = soup.select(".movie-poster")

        for item in movie_items:
            link_tag = item.find("a")
            img_tag = item.find("img")

            if link_tag and img_tag:
                movies.append({
                    "title": img_tag.get("alt"),
                    "image": img_tag.get("data-src") or img_tag.get("src"),
                    "link": "https://flixbaba.app" + link_tag.get("href")
                })

        return jsonify(movies)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
