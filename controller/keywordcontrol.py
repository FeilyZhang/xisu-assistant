from xml.dom.minidom import parse
import os


def select_keyword(keyword_str):
    # 读取配置文件路径
    xml_file_path = os.path.abspath("config/keyword.xml")
    dom = parse(xml_file_path)
    # 获取文件元素对象
    keywords = dom.documentElement
    # 读取配置文件中keyword_list数据
    keyword_list = keywords.getElementsByTagName("keyword")

    # 清空所有的关键字
    # KeyWordDao.drop_keyword_list()

    # 分别读取读取每个元素的值
    for keyword in keyword_list:
        # 取出3个标签对中的字符串
        key_name = keyword.getElementsByTagName("key-name")[0].firstChild.data
        if key_name in keyword_str:
            key_type = keyword.getElementsByTagName("key-type")[0].firstChild.data
            key_value = keyword.getElementsByTagName("key-value")[0].firstChild.data
            result_data = {
                "type": key_type,
                "result": key_value
            }
            return result_data
    return None
