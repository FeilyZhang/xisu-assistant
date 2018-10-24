from flask import Flask, request
import hashlib
from wechat.wechat import WeChat
from lxml import etree
from tools.logger import net_logger

from wechat import app

"""
整个项目的入口，get是验证用的，post是正常使用的接口
"""


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'weixin'
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if hashlib.sha1(s.encode('utf-8')).hexdigest() == signature:
            return echostr
        else:
            return ""
    else:
        # 读取request的信息并提取
        rec = request.stream.read()
        # 将信息转换成xml格式
        xml_rec = etree.fromstring(rec)
        net_logger.info("接受到" + xml_rec.find('FromUserName').text + "的消息")
        # 调用处理类对他进行处理
        wechat_obj = WeChat(xml_rec)
        # 返回处理结果
        content = wechat_obj.choose()
        net_logger.info("返回给" + xml_rec.find('FromUserName').text + "消息" + content)
        return content


