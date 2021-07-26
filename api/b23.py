from flask import Flask, request
import requests
import base64

app = Flask(__name__)


@app.route('/api/b23')
def b23():
    try:
        inputUrl = request.args.get('url')
        checkUrl = base64.b64decode(inputUrl).decode('utf-8')  # 确保url参数合法
    except:
        return 'The parameter "url" is incorrect.'

    if checkUrl[:7] == 'http://' or checkUrl[:8] == 'https://':
        sendUrl = 'http.lrhtony.cn://.bilibili.com/jump.html?key=' + inputUrl  # 处理最终链接
        data = {
            'build': 6180000,
            'buvid': 'test',
            'oid': sendUrl,
            'platform': 'android',
            'share_channel': 'COPY',
            'share_id': 'public.webview.0.0.pv',
            'share_mode': 3
        }
        try:
            html = requests.post("https://api.bilibili.com/x/share/click", data)  # 发送数据
        except:
            return 'Server request exception.'  # 处理请求错误或超时

        return html.text  # 返回官方结果
    else:
        return 'The link should include the "http" or "https" protocol header.'  # 筛选出不包含http/https请求头的链接


if __name__ == '__main__':
    app.debug = True
    app.run()
