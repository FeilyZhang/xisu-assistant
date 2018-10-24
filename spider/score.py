from bs4 import BeautifulSoup
from spider.login import Login
from tools.logger import spider_logger
import json
from config.configfile import TERM_ID


class Score(Login):
    def __init__(self, username, password):
        """
        继承父类登陆类，登陆后的操作是登陆类的子类，然后执行登陆操作，得到执行的结果
        :param username:账号
        :param password:密码
        """
        Login.__init__(self, username, password)
        self.flag = Login.login(self)

    def get_score(self):
        url = "http://jwxt.xisu.edu.cn/eams/teach/grade/course/person!search.action?semesterId="+TERM_ID+"&projectType="
        header = {
            'Host': 'jwxt.xisu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '67.0.3396.99 Safari/537.36',
            'Referer': 'http://jwxt.xisu.edu.cn/eams/login.action',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        try:
            r = self.sess.get(url, headers=header, timeout=15)
            text = r.text
            spider_logger.info("请求到成绩页面")
            return text
        except:
            return None

    def get_score_json(self):
        if self.flag is False:
            return None
        html = self.get_score()
        list1 = []
        soup = BeautifulSoup(html, 'html.parser')
        table_head = soup.find_all('thead')[0]
        th_list = []
        for th in table_head.find_all('th'):
            th_list.append(th.string)
        if '最终' not in th_list:
            return json.dumps('成绩未出')
        name_num = th_list.index('课程名称')
        credit_num = th_list.index('学分')
        total_num = th_list.index('最终')
        grade_point_num = th_list.index('绩点')

        table = soup.find_all('tr')
        for tr in table[1:]:
            td = tr.find_all('td')
            list1.append({'name': td[name_num].contents[0].replace('\n', '').replace('\r', '').replace('\t', ''),
                          'credit': td[credit_num].string.replace('\n', '').replace('\r', '').replace('\t', ''),
                          'total': td[total_num].string.replace('\r', '').replace('\t', '').replace(' ', '').
                         replace('\n', ''),
                          'grade_point': td[grade_point_num].string.replace('\n', '').replace('\r', '').replace('\t', '')
                          })
        json_str = json.dumps(list1)
        del list1
        del th_list
        return json_str



