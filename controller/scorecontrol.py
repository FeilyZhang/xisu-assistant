from dao.scoreDao import ScoreDao
from spider.score import Score
from dao.userDao import UserDao
from config.configfile import TERM_ID


def select_score(openid):
    """
    查成绩的逻辑有点复杂，每行都有注释
    :param openid:用户openid
    :return: 用户的成绩
    """
    # 初始化成绩数据库操作对象
    score_obj = ScoreDao(openid)
    # 如果数据库中无成绩
    score_database = score_obj.select_score(TERM_ID)
    # 从用户表中拿到用户信息
    user_info = UserDao.select_user_by_openid(openid)

    if score_database is None:
        # 使用用户信息调用爬虫，爬取用户成绩
        score = Score(user_info[0], user_info[1])
        score_str = score.get_score_json()
        if score_str is None:
            return None
        flag = score_obj.insert_score(score_str, TERM_ID)
        if flag is True:
            return select_score(openid)
        else:
            return None
    # 如果数据库的成绩更新时间不是今天
    elif score_obj.compare_score_time(score_database.updateTime.date()) is False:
        # 调用爬虫爬取时间
        score = Score(user_info[0], user_info[1])
        score_str = score.get_score_json()
        if score_str is None:
            return score_database.score
        flag = score_obj.update_score(score_str, TERM_ID)
        if flag is True:
            return select_score(openid)
        else:
            return score_database.score
    # 如果数据库中的成绩时间就是今天
    else:
        # 直接返回成绩数据
        return score_database.score
