#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import requests, re, json, time

app = Flask(__name__)

@app.route('/api/lanzous')
def lanzous():
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    try:
        url = request.args.get('url')  # 获取文件url
        if url == None:
            response = {
                'code': 404,
                'message': 'Input url error'
            }
            return jsonify(response)

        res = re.search('^(http(s)?://)?([-a-z]+\.)?lanzous.com/.*', url)
        if res:
            fileKey = url.split('/')[-1:][0]  # 获取文件key
        else:
            response = {
                'code': 404,
                'message': 'Input url error'
            }
            return jsonify(response)

        lanzousUrl = 'https://lanzous.com/' + fileKey  # 组合成新的链接，以防三级域名不同或不存在的情况
        startTime = time.time()
        print('startTime:', startTime)
        text_main = requests.get(lanzousUrl, headers=headers, timeout=3).text  # 发送请求，获取fn页面
        endTime = time.time()
        print('endTime:', endTime, 'use:', endTime - startTime)
        try:
            fn = re.findall('<iframe.* src="(.*?)".*</iframe>', text_main)[1]  # 提取fn页面path
        except:
            response = {
                'code': 404,
                'message': 'The input url is wrong, please check and try again. If the input is correct but the error still occurs, please contact me at feedback@lrhtony.cn, '
            }
            return jsonify(response)

        url_fn = 'https://lanzous.com' + fn  # 组合成fn链接
        startTime = time.time()
        print('startTime:', startTime)
        text_fn = requests.get(url_fn, headers=headers, timeout=3).text  # 请求fn页面内容
        endTime = time.time()
        print('endTime:', endTime, 'use:', endTime - startTime)
        ajaxdata = re.findall('''var ajaxdata = '(.*)';''', text_fn)[0]  # 提取里面的ajaxdata
        postData = re.findall('data : (.*),', text_fn)[1]  # 提取发送的数据
        postData = eval(postData)  # 变为字典数据，用eval是为了里面的变量ajaxdata可以获取的变量，该方法不安全
        headers['Content-Length'] = str(len(postData))  # 添加Content-Length，否则会返回错误数据
        headers['Referer'] = url_fn  # 添加Reffer，否则会返回错误数据
        startTime = time.time()
        print('startTime:', startTime)
        text_ajaxm = requests.post('https://lanzous.com/ajaxm.php', data=postData, headers=headers,timeout=3).text  # post发送数据
        endTime = time.time()
        print('endTime:', endTime, 'use:', endTime - startTime)
        json_ajaxm = json.loads(text_ajaxm)  # 转成字典类型
        fileZT = json_ajaxm['zt']  # 状态，1为可以下载
        fileDomain = json_ajaxm['dom']  # domain
        filePath = json_ajaxm['url']  # path
        if fileZT == 1:  # 判断状态，根据网页js改来，尚未遇到状态错误的情况
            fileURI_redirect = fileDomain + '/file/' + filePath  # 文件URI
        else:
            response = {
                'code': 500,
                'message': 'State error'
            }
            return jsonify(response)  # 状态错误

        del headers['Content-Length']  # 删除前面添加的headers
        del headers['Referer']
        startTime = time.time()
        print('startTime:', startTime)
        fileURI = requests.get(fileURI_redirect, headers=headers, allow_redirects=False).headers['Location']  # 获取经过重定向后的url
        endTime = time.time()
        print('endTime:', endTime, 'use:', endTime - startTime)
        response = {
            'code': 200,
            'message': fileURI
        }
        return jsonify(response)


    except(requests.exceptions.ConnectTimeout):
        response = {
            'code': 500,
            'message': 'Server request timed out, please try again'
        }
        return jsonify(response)

    except:
        response = {
            'code': 500,
            'message': 'Unknown error'
        }
        return jsonify(response)


if __name__ == '__main__':
    app.debug = True
    app.run()