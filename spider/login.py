import requests
import re
import hashlib
import time
from tools.logger import spider_logger
from proxy import server
"""
模拟登陆教务系统，使用Session，如果成功就返回一个成功session

"""


class Login:
    def __init__(self, username, password):
        """
        类初始化用户名密码，代理IP请求头以及请求的地址
        和登陆失败的次数
        :param username: 用户名
        :param password: 密码
        """
        # 初始化用户名密码
        self.username = username
        self.password = password
        # 初始化Session
        self.sess = requests.Session()
        # 拿到代理IP
        self.proxy = server.get_proxy()
        self.header = {
            'Host': 'jwxt.xisu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.index_url = "http://jwxt.xisu.edu.cn/eams/login.action"
        self.count = 0

    def get_index(self):
        """
        拿到首页的html
        如果出现连接错误
        换一个代理IP重试一遍
        """
        # 检查请求次数，如果超过三次返回失败
        if self.count >= 3:
            # 如果换了两个IP还不行返回失败
            return False
        # 尝试登陆，得到主页
        try:
            index_info = self.sess.get(self.index_url, headers=self.header, timeout=5)
            index_html = index_info.text

        # 如果发生网络链接异常，换个IP代理，并将失败次数加1，递归调用一遍自身
        except requests.exceptions.ConnectionError:
            self.count = self.count + 1
            spider_logger.warning("代理ip不可用" + str(self.count) + "次")
            self.proxy = server.get_proxy()
            return self.get_index()
        except requests.exceptions.ReadTimeout:
            return self.get_index()
        # 使用正则表达式匹配随即密钥字符串 例：1749ef8d-dfab-46c3-8cbb-5e46f0a83787-
        pattern = re.compile(
                '[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}-')
        secrete_str = pattern.findall(index_html)
        try:
            # 模拟浏览器JS代码对原始密码进行加密得到真实的登陆密码
            hash_str = secrete_str[0]
            hash_str = hash_str + self.password
            sha1 = hashlib.sha1()
            sha1.update(hash_str.encode('utf-8'))
            real_pass = sha1.hexdigest()
            # 返回真实密码
            return real_pass
        # 如果返回的页面不是正常的页面，无法解析出字符串，会出现secrete_str为空的状态，所以可以重新来一遍
        except IndexError:
            self.proxy = server.get_proxy()
            return self.get_index()

    def post_info(self, data):
        """
        提交表单，执行登陆操作
        :param data: 表单数据
        :return: True or False 返回登陆状态
        """
        try:
            # 提交表单
            result = self.sess.post(self.index_url, headers=self.header, data=data, timeout=30)
            # 如果登陆成功后应该跳转的页面
            true_url = 'http://jwxt.xisu.edu.cn/eams/home.action'
            # 如果登陆失败后应该跳转的页面
            false_url = 'http://jwxt.xisu.edu.cn/eams/login.action'
            # 让提交的返回头中的地址和上述的进行对比
            if result.url == true_url:
                return True
            elif result.url == false_url:
                return False
        # 如果发生连接错误，再来一遍
        except requests.exceptions.ConnectionError:
            self.post_info(data)
        except requests.exceptions.ReadTimeout:
            self.post_info(data)

    def login(self):
        # 先得到主页，拿到密码加密密钥
        real_pass = self.get_index()
        # 如果请求主页失败，返回空
        if real_pass is False:
            return False
        # 暂停一秒，防止触发网站防护
        time.sleep(1)
        # 准备好登陆需要的数据data
        data = {
            'username': self.username,
            'password': real_pass,
            'encodePassword': '',
            'session_locale': 'zh_CN'
        }
        # 登陆，返回登陆状态
        flag = self.post_info(data)
        # 如果登陆成功，返回session和代理IP
        return flag
