import json
import requests
from tools.wechatAccessToken import WeChatBase
from config.menu import MENU_JSON


class Menu(WeChatBase):
    def __init__(self):
        WeChatBase.__init__(self)

    def create(self):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % self.access_token
        post_data = json.dumps(MENU_JSON, ensure_ascii=False).encode('utf-8')
        result = requests.post(post_url, data=post_data)
        return result.text


a = Menu()
print(a.create())
