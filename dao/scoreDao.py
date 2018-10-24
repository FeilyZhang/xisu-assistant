import datetime
from tools.logger import database_logger
from dao.model import Scores, Session


class ScoreDao:
    """
    数据库成绩操作类,目前包括但不限于成绩的增加，更新，查询
    """
    def __init__(self, openid):
        self.openid = openid

    def compare_score_time(self, time_database):
        """
        比较是否需要更新成绩
        :param time_database: 从数据库中取得的数据
        :return: True OR False 数据库中是否存在今天的数据
        """
        time_now = datetime.datetime.now().date()
        result = time_now - time_database
        if result.days == 0:
            database_logger.info("用户" + self.openid + "数据库中已存在今天成绩")
            return True
        else:
            database_logger.info("用户" + self.openid + "今天未调取过爬虫")
            return False

    def insert_score(self, score_json, term_id):
        """
        向数据库中插入成绩
        :param score_json:成绩字符串
        :param term_id:学期字符串
        :return:True OR False
        """
        score_info = Scores()
        score_info.openid = self.openid
        score_info.score = score_json
        score_info.termStr = term_id
        score_info.updateTime = datetime.datetime.now().date()
        try:
            Session.add(score_info)
            Session.commit()
            database_logger.info("用户" + self.openid + "成绩插入成功")
            return True
        except:
            database_logger.info("用户" + self.openid + "成绩插入失败")
            return False

    def update_score(self, score_json, term_id):
        """
        数据库成绩更新函数
        :param score_json: 成绩字符串
        :param term_id: 学期字符串
        :return: True OR False
        """
        score_info = Session.query(Scores).filter_by(openid=self.openid, termStr=term_id).first()
        score_info.score = score_json
        score_info.updateTime = datetime.datetime.now().date()
        try:
            Session.commit()
            database_logger.info("用户" + self.openid + "成绩更新成功")
            return True
        except:
            database_logger.error("用户" + self.openid + "成绩查询失败")
            return False

    def select_score(self, term_id):
        """
        查询成绩是否存在，如果没有，返回不存在
        :param term_id: 学期字符串
        :return: None OR score_info 空或者成绩对象
        """
        score_info = Session.query(Scores).filter_by(openid=self.openid, termStr=term_id).first()
        if score_info is None:
            database_logger.warning("用户" + self.openid + "数据库无成绩")
            return None
        else:
            return score_info

    def delete_score(self, term_id):
        """
        用户
        :param term_id:
        :return:
        """
        try:
            score_info = Session.query(Scores).filter_by(openid=self.openid, termStr=term_id).all()
            if score_info:
                Session.delete(score_info)
                database_logger.info('用户'+self.openid+'删除成绩成功')
                Session.commit()
                return True
        except:
            database_logger.info('用户'+self.openid+'删除成绩失败')
            return False



