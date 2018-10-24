from tools.logger import database_logger
from dao.model import Session, Course


class CourseDao:
    """
    课表查询数据库封装类，有插入和查询操作
    """
    def __init__(self, openid):
        """
        初始化openid
        :param openid:openid
        """
        self.openid = openid

    def insert_course(self, term_id, course_str):
        """
        插入课表函数
        :param term_id:学期ID
        :param course_str: 学期课表json字符串
        :return:True OR False
        """
        course = Course()
        course.openid = self.openid
        course.term_id = term_id
        course.course_str = course_str
        try:
            Session.add(course)
            Session.commit()
            database_logger.info("用户" + self.openid + "课表插入成功")
            return True
        except:
            database_logger.info("用户" + self.openid + "课表插入失败")
            return False

    def select_course(self, term_id):
        """
        查询函数
        :param term_id: 学期ID
        :return: 课表信息，是个json
        """
        course_info = Session.query(Course).filter_by(openid=self.openid, term_id=term_id).first()
        if course_info is None:
            database_logger.warning("用户" + self.openid + "数据库无课表")
            return None
        else:
            return course_info

    def delete_course(self, term_id):
        """
        用户删除课表
        :param term_id:学期代号
        :return:True OR False
        """
        try:
            course_info = Session.query(Course).filter_by(openid=self.openid, termStr=term_id).first()
            if course_info:
                Session.delete(course_info)
                database_logger.info('用户'+self.openid+'删除课表成功')
                Session.commit()
                return True
        except:
            database_logger.info('用户'+self.openid+'删除课表失败')
            return False
