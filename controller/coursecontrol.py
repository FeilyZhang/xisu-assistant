from dao.courseDao import CourseDao
from dao.userDao import UserDao
from config.configfile import TERM_ID
from spider.curriculum import Curriculum


def select_course_control(openid):
    course_dao = CourseDao(openid)
    course_database = course_dao.select_course(TERM_ID)
    # 从用户表中拿到用户信息
    user_info = UserDao.select_user_by_openid(openid)
    if course_database is None:
        # 使用用户信息调用爬虫，爬取用户课表
        course = Curriculum(user_info[0], user_info[1])
        score_str = course.parse_curriculum_page()
        if score_str is None:
            return None
        flag = course_dao.insert_course(TERM_ID, score_str)
        if flag is True:
            return select_course_control(openid)
        else:
            return None
    else:
        return course_database.course_str
