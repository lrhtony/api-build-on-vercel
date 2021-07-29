from flask import Flask, request, jsonify
from geoip import geolite2

app = Flask(__name__)


@app.route('/api/sou/location')
def get():
    try:
        match = geolite2.lookup(request.remote_addr)
        # match = geolite2.lookup('121.32.35.129')
        return jsonify({
            'code': 200,
            'ip': match.ip,
            'country': match.country,
            'location': match.location,
            'message': ''
        })
    except AttributeError as e:
        return jsonify({
            'code': -404,
            'message': str(e)
        })


if __name__ == '__main__':
    app.debug = True
    app.run()
