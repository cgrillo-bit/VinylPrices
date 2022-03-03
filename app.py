from flask import Flask, jsonify
from client import discogs_search

app = Flask(__name__)


@app.route('/send/', methods=['POST'])
def search(artist, album):
    return jsonify({
        "meta": {
            "status": 200,
        },
        "artist": artist,
        "album": album
    })
