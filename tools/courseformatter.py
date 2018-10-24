import json
import datetime
from config.configfile import TERM_START_TIME


class CalCourse:
    """
    拿到一个从数据库取出的json字符串，处理后返回今天该上的课的信息
    """
    def __init__(self, course_json_str):
        # 将字符串解析成list
        self.data_course = json.loads(course_json_str)

    @staticmethod
    def check_weekly(start_time):
        """
        判断是周几
        :param start_time:上课开始节数
        :return: 返回今天是否有这节课
        """
        # 得到今天是周几
        d = datetime.datetime.now()
        # 得到开始节数的周数
        class_weekly = int(start_time) // 12
        # 如果相同返回今天有这个课
        if d.weekday() == class_weekly:
            return True
        else:
            return False

    @staticmethod
    def cal_class_time(start_time, end_time):
        """
        计算开课第几节课
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return:开课字符串
        """
        # 得到今天的开始节数
        start_class_num = int(start_time) % 12 + 1
        # 计算这节课占用几个课时
        end_class_num = int(end_time) - int(start_time) + start_class_num
        return "第"+str(start_class_num)+" - "+str(end_class_num)+"节"

    @staticmethod
    def cal_weekly(weeks_time):
        """
        计算当前日期是教学周的第几周,是否上课
        :param weeks_time:该周是否上课的0，1串
        :return: True OR False
        """
        # 得到当前日期相对于周数
        weeks = datetime.datetime.now().strftime("%W")
        # 得到开学日期相对于周数
        start_date = datetime.datetime.strptime(TERM_START_TIME, '%Y-%m-%d')
        # 相减得到当前日期是教学周的第几周
        week_num = int(weeks) - int(start_date.strftime('%W'))
        # 将开课周数字符串分割成list
        list_weeks = list(weeks_time)
        # 判断当前周数是否开课
        if list_weeks[week_num] == '1':
            return True
        else:
            return False

    def formatter(self):
        """
        格式化函数，处理字符串，返回一个微信可以返回的结果
        :return:
        """
        # 初始化返回字符串
        result_str = ''
        # 初始化今天要上的课程
        count = 0
        # 循环所有课程
        for course in self.data_course:
            # 拿到课程信息
            class_name = course["class_name"]
            class_room = course["class_room"]
            class_teacher = course["teacher"]
            weeks_time = course["class_weeks"]
            start_time = course["start_time"]
            end_time = course["end_time"]
            # 如果该课程是今天
            if self.check_weekly(start_time) is True:
                # 如果该课程这周上
                if self.cal_weekly(weeks_time) is True:
                    # 将今天上的课程数加一
                    count = count + 1
                    # 加入该课程的信息(名称，教师，老师，第几节）
                    temp = [class_name, class_room, class_teacher, self.cal_class_time(start_time, end_time)]
                    result_str += '\n'.join(temp)
                    result_str += '\n\n'
        result_str = "今天你有"+str(count)+"门课\n\n" + result_str
        if count == 0:
            result_str ="今天无课哦"
        return result_str
