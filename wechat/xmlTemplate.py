import time


class Template:

    @staticmethod
    def return_text_xml(xml, content):
        from_user = xml.find("FromUserName").text
        to_user = xml.find("ToUserName").text
        return_xml = """<xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%d</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                        </xml>""" % (from_user, to_user, int(time.time()), content)
        return return_xml

    @staticmethod
    def return_image_xml(xml, image_url):
        from_user = xml.find("FromUserName").text
        to_user = xml.find("ToUserName").text
        return_xml = """< xml >
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%d</CreateTime>
                        <MsgType><![CDATA[image]]></MsgType>
                        <PicUrl><![CDATA[%s]]></PicUrl>
                        </xml>""" % (from_user, to_user, int(time.time()), image_url)
        return return_xml