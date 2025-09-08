from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "ברוך הבא ל־Flixbaba API!", "status": "online"})

@app.route('/movies')
def get_movies():
    url = 'https://flixbaba.app'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = []

    for card in soup.select('.MuiCard-root'):
        title = card.select_one('.MuiTypography-h5')
        image = card.select_one('img')
        link = card.find('a')

        if title and image and link:
            movies.append({
                'title': title.text.strip(),
                'image': image['src'],
                'link': url + link['href']
            })

    return jsonify(movies)
