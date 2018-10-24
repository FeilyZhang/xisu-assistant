from dao.userDao import UserDao
from dao.scoreDao import ScoreDao
from dao.courseDao import CourseDao
from spider.login import Login
from config.configfile import TERM_ID

"""
用户操作逻辑层，所有逻辑判断在这一层，其他层只负责封装操作。
"""


def binding_control(user_info):
    """
    绑定逻辑
    :param user_info:用户信息
    :return:True OR False 绑定是否成功
    """
    flag = UserDao.select_user_flag(user_info["openid"])
    login_obj = Login(user_info["username"], user_info["password"])
    if flag == 1:
        if login_obj.login() is True:
            return UserDao.insert_user(user_info)
        else:
            return "用户名密码可能错误\n或者教务系统网络不可达"
    elif flag == 2:
        if login_obj.login() is True:
            return UserDao.update_user(user_info)
        else:
            return "用户名密码可能错误\n或者教务系统网络不可达"
    else:
        return "你已绑定"


def cancel_binding_control(openid):
    """
    解除绑定逻辑
    :param openid:需要解除绑定的openid
    :return:True OR False 解绑是否成功
    """
    flag = UserDao.select_user_flag(openid)
    if flag == 3:
        # 删除成绩
        score_obj = ScoreDao(openid)
        score_obj.delete_score(TERM_ID)
        # 删除课表
        course_obj = CourseDao(openid)
        course_obj.delete_course(TERM_ID)
        return UserDao.delete_user(openid)
    else:
        return False


def select_user_info_control(openid):
    """
    查询用户信息逻辑
    :param openid:用户openid
    :return:用户信息 [username, password] 或者为空
    """
    flag = UserDao.select_user_flag(openid)
    if flag == 3:
        return UserDao.select_user_by_openid(openid)
    else:
        return None
