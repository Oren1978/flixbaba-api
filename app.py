from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

# URL של ה-API הפנימי של Flixbaba
FLIXBABA_API_URL = "https://be.flixbaba.tv/media"
HEADERS = {
    "Origin": "https://flixbaba.app",
    "Referer": "https://flixbaba.app/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

@app.route("/")
def index():
    return jsonify({"message": "ברוך הבא ל-Flixbaba API!", "status": "online"})

@app.route("/movies", methods=["GET"])
def get_movies():
    try:
        # שליחת בקשה ל-API הפנימי של Flixbaba
        params = {"mediaType": "movie", "page": 1, "limit": 50}
        response = requests.get(FLIXBABA_API_URL, headers=HEADERS, params=params)
        response.raise_for_status()

        data = response.json()
        movies_raw = data.get("items", [])

        # סינון ועיצוב הנתונים לפורמט נקי
        movies = []
        for m in movies_raw:
            title = m.get("title")
            poster = m.get("poster")
            # לוודא שיש לנו נתונים רלוונטיים לפני הוספה
            if title and poster:
                movies.append({
                    "id": m.get("id"),
                    "title": title,
                    "poster": poster,
                    "year": m.get("releaseDate"),
                    "link": f"https://flixbaba.app/movie/{m.get('id')}/{m.get('slug')}/watch"
                })

        return jsonify(movies)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
