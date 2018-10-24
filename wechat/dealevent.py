from tools.logger import net_logger


def deal_event(xml):
    event = xml.find("Event").text
    if event == "subscribe":
        net_logger.info("关注操作")
        return "subscribe"
    elif event == "CLICK":
        net_logger.info("点击菜单" + xml.find("EventKey").text)
        return xml.find("EventKey").text
    else:
        return "else"