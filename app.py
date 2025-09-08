from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/movies", methods=["GET"])
def get_movies():
    url = "https://flixbaba.app/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    soup = BeautifulSoup(response.text, "html.parser")
    movies = []

    # מצא כרטיסי סרטים לפי מחלקה
    for card in soup.select("a.MuiCardActionArea-root"):
        title = card.get("title") or card.text.strip()
        link = "https://flixbaba.app" + card.get("href")
        image_tag = card.select_one("img")
        image = image_tag.get("src") if image_tag else None

        movies.append({
            "title": title,
            "link": link,
            "image": image
        })

    return jsonify(movies)

if __name__ == "__main__":
    app.run(debug=True)
