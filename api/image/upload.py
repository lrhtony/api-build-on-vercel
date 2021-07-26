from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/api/image/upload')
def upload_image():
    try:
        method = request.args.get('method')
        return None
    except:
        pass


if __name__ == '__main__':
    app.debug = True
    app.run()
