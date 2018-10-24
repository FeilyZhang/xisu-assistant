from tools.logger import database_logger
from dao.model import User, engine, Session
from sqlalchemy.sql import text


class UserDao:
    """
    数据库封装的用户操作，有增删改查。
    """

    @staticmethod
    def select_user_flag(openid_str):
        """
        查看该用户是否可以进行绑定,静态函数
        :param openid_str: openid
        :return:用户绑定状态，1：用户名空，2：用户以解绑，2：用户已绑定
        """
        db_connect = engine.connect()
        result = db_connect.execute(text('select flag from user where openid=:openid'), openid=openid_str)
        if result.rowcount <= 0:
            database_logger.info("用户名 " + openid_str + " 为空")
            return 1
        result_flag = result.fetchall()[0][0]
        if result_flag == 1:
            database_logger.info("用户名 " + openid_str + " 处于绑定状态")
            return 3
        elif result_flag == 0:
            database_logger.info("用户名 " + openid_str + " 处于解绑状态")
            return 2

    @staticmethod
    def select_user_by_openid(openid):
        """
        通过openid查找用户信息
        :param openid:openid
        :return:用户账号和密码
        """
        user = Session.query(User).filter_by(openid=openid).first()
        return user.username, user.password

    @staticmethod
    def insert_user(user_info):
        """
        用户插入函数
        :param user_info:用户信息，json数据
        :return: True OR False
        """
        user = User()
        user.openid = user_info["openid"]
        user.username = user_info["username"]
        user.password = user_info["password"]
        try:
            Session.add(user)
            Session.commit()
            database_logger.info("用户" + user.openid + "用户绑定成功")
            return True
        except:
            database_logger.error("用户" + user.openid + "用户绑定失败")
            return False

    @staticmethod
    def update_user(user_info):
        """
        用户更新函数，修改绑定标志为1
        :param user_info:
        :return:
        """
        try:
            user = Session.query(User).filter_by(openid=user_info["openid"]).first()
            user.username = user_info["username"]
            user.password = user_info["password"]
            user.flag = 1
            Session.commit()
            database_logger.info("用户" + user_info["openid"] + "用户更新成功")
            return True
        except:
            database_logger.error("用户" + user_info["openid"] + "用户绑定失败")
            return False

    @staticmethod
    def delete_user(openid):
        """
        解除绑定，修改绑定标志为0
        :param openid:openid
        :return:True OR False 用户解绑信息
        """
        try:
            user = Session.query(User).filter_by(openid=openid).first()
            user.flag = 0
            Session.commit()
            database_logger.info("用户" + openid + "解绑成功")
            return True
        except:
            database_logger.error("用户" + openid + "解绑失败")
            return False



