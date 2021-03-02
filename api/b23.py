from flask import Flask, request
import requests
import base64
app = Flask(__name__)

@app.route('/api/b23')
def post():
    url = request.args.get('url')
    url = base64.b64decode(url).decode("utf-8")
    data = {
        'build': 6180000,
        'buvid': 'test',
        'oid': url,
        'platform': 'android',
        'share_channel': 'COPY',
        'share_id': 'public.webview.0.0.pv',
        'share_mode': 3
    }
    html = requests.post("https://api.bilibili.com/x/share/click", data)
    return html.text