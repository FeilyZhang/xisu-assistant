from bs4 import BeautifulSoup
from spider.login import Login
from tools.logger import spider_logger
import re
import json
from config.configfile import TERM_ID


class Curriculum(Login):
    """
    课程表抓取类
    """
    def __init__(self, username, password):
        """
        继承自登陆类，负责爬取和解析课表页面
        :param username:用户名
        :param password:密码
        """
        Login.__init__(self, username, password)
        self.flag = Login.login(self)

    def get_curriculum_page(self):
        """
        此函数完成的功能是拿到课表页面
        :return:
        """
        # 请求基础页面，拿到学生ID(student_id),请求页面地址和头部如下
        get_student_num_url = "http://jwxt.xisu.edu.cn/eams/courseTableForStd.action"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Referer": "http://jwxt.xisu.edu.cn/eams/courseTableForStd!courseTable.action"
        }
        page_has_student_number = self.sess.get(get_student_num_url, headers=headers, timeout=15)
        # 使用正则表达式拿到页面的student_id
        find_student_id = re.compile(r'"(?<=ids",")\d*(?=")')
        student_id = re.findall(find_student_id, page_has_student_number.text)[0].replace('"', '')
        # 使用拿到的ID 构建真正课表页面的url
        get_curriculum_page_url = "http://jwxt.xisu.edu.cn/eams/courseTableForStd!courseTable.action" \
                                  "?semester.id="+TERM_ID+"&setting.kind=std&ids="+student_id
        page_has_curriculum = self.sess.get(get_curriculum_page_url, headers=headers, timeout=15)
        curriculum_html = page_has_curriculum.text
        spider_logger.info("请求到课表页面")
        # 返回拿到的页面
        return curriculum_html

    def parse_curriculum_page(self):
        """
        解析课表页面函数，去掉页面无用的干扰
        :return: 课表json字符串
        """
        # 拿到课表页面
        curriculum_html = self.get_curriculum_page()
        # 使用beautifulSoup解析
        soup = BeautifulSoup(curriculum_html, 'html.parser')
        # 拿到js代码
        js_data = soup.findAll("script", language="JavaScript")[-1].text

        # 使用正则表达式找到含有教师列表的字符串
        find_str_has_teacher_name = re.compile(r'var teachers.*')
        str_has_teacher = re.findall(find_str_has_teacher_name, js_data)
        # 作最后的处理，去掉无用的字符
        teacher_list = []
        find_teacher_name = re.compile(r'(?<=")\w*(?=")')
        for teacher in str_has_teacher:
            teacher_name = re.findall(find_teacher_name, teacher)
            teacher_list = teacher_list + teacher_name

        # 找到含有课程信息的字符串
        find_str_has_curriculum_info = re.compile(r'activity = new TaskActivity.*')
        curriculum_str = re.findall(find_str_has_curriculum_info, js_data)

        # 找到js中计算开课时间的字符串
        find_str_has_curriculum_time = re.compile(r'index =\d.unitCount.\d+')
        str_has_curriculum_time = re.findall(find_str_has_curriculum_time, js_data)
        find_curriculum_time = re.compile(r'\d+')
        curriculum_times = []
        for curriculum_time in str_has_curriculum_time:
            curriculum_time = re.findall(find_curriculum_time, curriculum_time)
            curriculum_times = curriculum_times + curriculum_time

        # 作最后处理，将开课时间和授课教师和课程信息组成一个json数组
        curriculum_list = []
        find_curriculum_str = re.compile(r'\d+.*0')
        for i, curriculum_info in enumerate(curriculum_str):
            final_curriculum_str = re.findall(find_curriculum_str, curriculum_info)[0].split('","')
            curriculum_list.append({
                'class_name': final_curriculum_str[1],
                'class_room': final_curriculum_str[3],
                'class_weeks': final_curriculum_str[4],
                'teacher': teacher_list[i],
                'start_time': int(curriculum_times[i * 4]) * 12 + int(curriculum_times[i * 4 + 1]),
                'end_time': int(curriculum_times[i * 4 + 2]) * 12 + int(curriculum_times[i * 4 + 3])
            })
        json_str = json.dumps(curriculum_list)
        return json_str
