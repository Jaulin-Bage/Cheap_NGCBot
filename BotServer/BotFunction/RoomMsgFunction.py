from BotServer.BotFunction.InterfaceFunction import *
from ApiServer.ApiMainServer import ApiMainServer
from BotServer.BotFunction.JudgeFuncion import *
from DbServer.DbMainServer import DbMainServer
import Config.ConfigServer as Cs


class RoomMsgFunction:
    def __init__(self, wcf):
        """
        群聊消息功能类, 撤回消息检测, 群聊消息总结, 群聊消息排行榜
        :param wcf:
        """
        self.wcf = wcf
        self.Dms = DbMainServer()
        self.Ams = ApiMainServer()
        configData = Cs.returnConfigData()
        self.summarizeMsgKeyWords = configData['functionKeyWord']['summarizeMsgWord']
        self.speechListKeyWords = configData['functionKeyWord']['speechListWord']
        self.rowingListKeyWords = configData['functionKeyWord']['rowingListWord']

    def mainHandle(self, message):
        msgType = message.type
        msgId = message.id
        roomId = message.roomid
        sender = message.sender
        content = message.content.strip()
        senderName = getIdName(self.wcf, sender)

        # 把文本消息完整存入到数据库
        
        if msgType == 10002:
            newMsgId = getWithdrawMsgData(content)
            if newMsgId:
                oldMsg = self.Dms.searchRoomContent(roomId, newMsgId)
                msg = f'拦截到一条撤回的消息\n发送ID: {oldMsg[1]}\n发送人: {oldMsg[2]}\n消息类型: {oldMsg[0]}\n消息类容: {oldMsg[3]}'
                self.wcf.send_text(msg, receiver=roomId)
        else:
            # 其它类型消息不存内容
            pass
