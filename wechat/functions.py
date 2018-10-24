from controller.usercontrol import cancel_binding_control, select_user_info_control
from dao.userDao import UserDao
from controller.scorecontrol import select_score
from controller.coursecontrol import select_course_control
from config.configfile import HOST_NAME
from tools.courseformatter import CalCourse
import json


def cancel_binding(from_user):
    if cancel_binding_control(from_user) is True:
        result_str = '解绑成功'
    else:
        result_str = '解绑失败，您未绑定'
    return result_str


def binding(from_user):
    flag = UserDao.select_user_flag(from_user)
    if flag != 3:
        data = "<a href='"+HOST_NAME+"/binding?openid=%s'>点击绑定</a>" % from_user
    else:
        user_info = select_user_info_control(from_user)
        username = user_info[0]
        password = user_info[1]
        data = '您已绑定,您的绑定信息为\n用户名：{username}\n密  码：{password}'.format(username=username, password=password)
    return data


def find_score(from_user):
    flag = UserDao.select_user_flag(from_user)
    if flag != 3:
        data = '您未绑定'
        return data

    # 调取后台接口，获取成绩的数据
    score = select_score(from_user)
    if score is None:
        data = '网络繁忙，稍后再试'
        return data
    else:
        data_score = json.loads(score)
        if data_score == '成绩未出':
            data = '成绩未出'
            return data
        else:
            data = ''
            grade_point_num_total = 0.0
            for score in data_score:
                grade_point_num_total += float(score['grade_point'])
                data += score['name'] + ":\n成绩：" + score['total'] + "\n\n"
            data += "平均绩点：" + str(round(grade_point_num_total / len(data_score), 1)) + "\n"
            data += "<a href='"+HOST_NAME+"/score?openid=%s'>详细成绩</a>" % from_user
            return data


def select_course(from_user):
    flag = UserDao.select_user_flag(from_user)
    if flag != 3:
        data = '您未绑定'
        return data

    # 调取后台接口，获取成绩的数据
    course = select_course_control(from_user)
    if course is None:
        data = '网络繁忙，稍后再试'
        return data
    else:
        course_obj = CalCourse(course)
        result_str = course_obj.formatter()
        return result_str
