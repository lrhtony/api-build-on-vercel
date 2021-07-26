from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)


@app.route("/api/bing-img")
def get_img():
    info_page = requests.get('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1').text
    info = json.loads(info_page)
    url = info['images'][0]['url']
    text = info['images'][0]['copyright']
    return jsonify({
        'url': 'https://bing.com' + url,
        'copyright': text
    })



