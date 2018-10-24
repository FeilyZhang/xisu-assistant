import requests
from config.configfile import APP_ID, APP_SECRET
import json
from tools.redisClient import RedisAccessToken


class WeChatBase:
    def __init__(self):
        self.access_token = self.get_access_token()

    @staticmethod
    def get_access_token_from_net():
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(APP_ID, APP_SECRET)
        result = requests.get(url)
        access_token = json.loads(result.text).get('access_token')
        return access_token

    def get_access_token(self):
        """
        从数据库中拿到access_token,如果数据库中没有，就从网络上
        :return:
        """
        redis_token = RedisAccessToken()
        token_from_redis = redis_token.get_access_token()
        if token_from_redis is None:
            flag = redis_token.add_access_token(self.get_access_token_from_net())
            if flag is True:
                return redis_token.get_access_token()
            else:
                return False
        else:
            return token_from_redis


if __name__ == '__main__':
    result = WeChatBase()
    # print(result.add_access_token('123354435'))
    print(result.access_token)
