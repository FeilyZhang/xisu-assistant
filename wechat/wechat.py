from controller.keywordcontrol import select_keyword
from wechat.dealevent import deal_event
from wechat.xmlTemplate import Template
from wechat.functions import binding, cancel_binding, find_score, select_course


class WeChat(object):
    """
    后台操作预处理和入口
    """

    def __init__(self, xml):
        self.xml = xml

    def choose(self):
        """
        对xml进行处理，并且
        :return:
        """
        msg_type = self.xml.find("MsgType").text
        if msg_type == 'event':
            keyword = deal_event(self.xml)
        elif msg_type == 'text':
            keyword = self.xml.find("Content").text
        else:
            keyword = "else"

        # 去掉空格
        keyword = keyword.strip()

        if keyword != "":
            result_key = select_keyword(keyword)
            if result_key is not False:
                content = self.content_receive(result_key)
            else:
                return ""
            return_xml = Template.return_text_xml(self.xml, content)
            return return_xml

    def content_receive(self, data_info):
        data_type = data_info["type"]
        if data_type == "text":
            return data_info["result"]
        elif data_type == "function":
            function_name = data_info["result"]
            if function_name == 'selectScore':
                data = find_score(self.xml.find("FromUserName").text)
                return data
            elif function_name == 'add':
                data = binding(self.xml.find("FromUserName").text)
                return data
            elif function_name == 'delete':
                data = cancel_binding(self.xml.find("FromUserName").text)
                return data
            elif function_name == 'selectCourse':
                data = select_course(self.xml.find("FromUserName").text)
                return data
            else:
                return ""



