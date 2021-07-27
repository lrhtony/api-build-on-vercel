from flask import Flask, request

app = Flask(__name__)


@app.route('/api/ip-test')
def get_ip():
    return request.remote_addr


if __name__ == '__main__':
    app.debug = True
    app.run()
