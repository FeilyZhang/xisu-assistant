#西安外国语大学小助手
使用爬虫技术爬取教务系统，
目前代理池出BUG，暂时使用真实IP，未出现封禁IP的情况，
对教务系统研究不透彻，并且没有人指点如何高效写爬虫，爬虫模块目前并不是最优的。
数据库使用mysql，由于用户量不大，没有数据访问瓶颈。
其他辅助的存储工具有：redis负责存储代理IP信息，xml负责存储微信公众号自动回复（用户每次操作微信都要查询mysql数据库，虽未出现瓶颈，但是总归不是个适合关系数据库存储的数据，下一版本将使用xml文件实现，暂时使用mysql代替）
目前实现的功能有，成绩查询，和绑定功能，整个工程使用mvc模式，底层mysql数据库操作封装，爬虫封装，代理池封装，微信前端使用flask封装，有完整的日志功能，同时对不同的运行环境需要的参数使用配置文件的全局变量实现。
主要配置项：
```
#代理IP池相关
# 代理IP池校验器校验地址
VALIDATOR_BASE_URL = "https://www.baidu.com/"
# 校验器循环周期（分钟）
VALIDATOR_RUN_CYCLE = 15
# 爬取器循环周期（分钟）
CRAWLER_RUN_CYCLE = 30

#微信公众号配置相关
APP_ID = ""
APP_SECRET = ""

# 网站配置
# 网站url前缀
HOST_NAME = "http://dab071ab.ngrok.io"

#数据库配置
# 数据库连接字符串
DATABASE_URL = "mysql+pymysql://sujunhao:sujunhao@localhost:3306/wechat?charset=utf8mb4"

#教务系统


```

新手项目，第一次写markdown文件。