from BotServer.BotFunction.InterfaceFunction import *
from ApiServer.ApiMainServer import ApiMainServer
from BotServer.BotFunction.JudgeFuncion import *
from DbServer.DbMainServer import DbMainServer
import Config.ConfigServer as Cs


class PointFunction:
    def __init__(self, wcf):
        """
        积分功能
        :param wcf:
        """
        self.wcf = wcf
        self.Ams = ApiMainServer()
        self.Dms = DbMainServer()
        configData = Cs.returnConfigData()
        self.threatBookWords = configData['functionKeyWord']['threatBookWord']
        self.aiPicKeyWords = configData['functionKeyWord']['aiPic']
        self.searchPointKeyWord = configData['pointConfig']['queryPointWord']
 
    def mainHandle(self, message):
        content = message.content.strip()
        sender = message.sender
        roomId = message.roomid
        msgType = message.type
        senderName = self.wcf.get_alias_in_chatroom(sender, roomId)
        atUserLists, noAtMsg = getAtData(self.wcf, message)
        if msgType == 1:
            if judgeAtMe(self.wcf.self_wxid, content, atUserLists) and not judgeOneEqualListWord(noAtMsg,
                                                                                                   self.aiPicKeyWords):
                aiMsg = self.Ams.getAi(noAtMsg)
                if aiMsg:
                    
                    head = '本消息由ai生成，不具备法律效益！\n'
                    self.wcf.send_text(f'@{senderName} {head}{aiMsg}',
                                       receiver=roomId, aters=sender)
                    return
                self.wcf.send_text(
                    f'@{senderName} Ai对话接口出现错误, 请联系超管查看控制台输出日志',
                    receiver=roomId, aters=sender)
            # Ai画图
            elif judgeAtMe(self.wcf.self_wxid, content, atUserLists) and judgeOneEqualListWord(noAtMsg,
                                                                                               self.aiPicKeyWords):
                aiPicPath = self.Ams.getAiPic(noAtMsg)
                if aiPicPath:
                    self.wcf.send_image(path=aiPicPath, receiver=roomId)
                    return
                self.wcf.send_text(
                    f'@{senderName} Ai画图接口出现错误, 请联系超管查看控制台输出日志',
                    receiver=roomId, aters=sender)
            