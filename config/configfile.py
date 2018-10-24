"""
配置文件模块
读取配置文件并处理
"""

# 请求超时时间（秒）
REQUEST_TIMEOUT = 15
# 请求延迟时间（秒）
REQUEST_DELAY = 0

# redis 地址
REDIS_HOST = "localhost"
# redis 端口
REDIS_PORT = 6379
# redis 密码
REDIS_PASSWORD = None
# redis set key
REDIS_KEY = "proxies:ranking"
# redis 连接池最大连接量
REDIS_MAX_CONNECTION = 20

# REDIS SCORE 最大分数
MAX_SCORE = 10
# REDIS SCORE 最小分数
MIN_SCORE = 0
# REDIS SCORE 初始分数
INIT_SCORE = 9


# 批量测试数量
VALIDATOR_BATCH_COUNT = 256
# 校验器测试网站，可以定向改为自己想爬取的网站，如新浪，知乎等
VALIDATOR_BASE_URL = "https://www.baidu.com/"
# 校验器循环周期（分钟）
VALIDATOR_RUN_CYCLE = 15


# 爬取器循环周期（分钟）
CRAWLER_RUN_CYCLE = 30
# 请求 headers
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}
# 微信公众号配置
APP_ID = "wx8fa5999240539cbc"
APP_SECRET = "77c23db2af248a6bd45ecca84b31917c"

REDIS_ACCESSTOKEN_KEY = 'wx:ACCESS_TOKEN'

# 网站配置
HOST_NAME = " http://02c445b4.ngrok.io"


# 数据库连接字符串
DATABASE_URL = "mysql+pymysql://sujunhao:sujunhao@localhost:3306/wechat?charset=utf8mb4"

# 学期代号
# 2017-2018 2 ID is 29
# 2018-2019 1 ID is 11
# 2018-2019 2 ID is 30
# 2019-2020 1 ID is 12
# 2019-2020 2 ID is 31
# 2020-2021 1 ID is 47
# 2020-2021 2 ID is 48

# def cal_term_ID():
#

TERM_ID = "11"
# 开学日期（校历计算，算当前周是第几周）上课日期第一天
TERM_START_TIME = '2019-9-3'
