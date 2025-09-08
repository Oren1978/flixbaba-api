from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# הגדרות כלליות
BASE_URL = "https://flixbaba.app/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

@app.route("/")
def index():
    return jsonify({"message": "ברוך הבא ל-Flixbaba API!", "status": "online"})

@app.route("/movies", methods=["GET"])
def get_movies():
    try:
        # שלב 1: שליפת עמוד הבית של האתר
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        movies = []
        
        # שלב 2: מציאת כל קופסאות הסרטים
        movie_items = soup.select(".movie-item-style-2")

        # שלב 3: חילוץ נתונים מכל סרט
        for item in movie_items:
            image_tag = item.select_one("img.lozad")
            title_tag = item.select_one("h6 a")

            if image_tag and title_tag:
                title = title_tag.text.strip()
                image_url = image_tag.get("data-src")
                movie_page_url = title_tag.get("href")

                if title and image_url and movie_page_url:
                    full_image_url = f"{BASE_URL}{image_url}"
                    full_movie_page_url = f"{BASE_URL}{movie_page_url}"

                    movies.append({
                        "title": title,
                        "image": full_image_url,
                        "page_url": full_movie_page_url
                    })

        return jsonify(movies)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
