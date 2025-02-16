from BotServer.BotFunction.InterfaceFunction import *
from ApiServer.AiServer.AiDialogue import AiDialogue
from BotServer.BotFunction.JudgeFuncion import *
from DbServer.DbMainServer import DbMainServer
import Config.ConfigServer as Cs
from OutPut.outPut import op
from threading import Thread


class FriendMsgHandle:
    def __init__(self, wcf):
        """
        关键词拉群 yes
        好友消息转发给超管 yes
        好友Ai消息 yes
        自定义关键词回复 yes
        管理员公众号消息转发给推送群聊 yes
        查看白名单群聊 yes
        查看黑名单群聊 yes
        查看推送群聊 yes
        查看黑名单公众号 yes
        好友红包消息处理 yes
        好友转账接收 yes 微信版本过低无法使用
        :param wcf:
        """
        self.wcf = wcf
        self.Ad = AiDialogue()
        self.Dms = DbMainServer()
        configData = Cs.returnConfigData()
        # 超级管理员列表
        self.Administrators = configData['Administrators']
        # 给好友发消息关键词
        self.sendMsgKeyWords = configData['adminFunctionWord']['sendMsgWord']
        # Ai锁
        self.aiLock = configData['systemConfig']['aiLock']
        # 进群关键词字典
        self.roomKeyWords = configData['roomKeyWord']
        # 好友消息转发给管理员开关
        self.msgForwardAdmin = configData['systemConfig']['msgForwardAdmin']

    def mainHandle(self, msg):
        content = msg.content.strip()
        sender = msg.sender
        msgType = msg.type

        if msgType == 1:
            # 关键词进群
            if judgeEqualListWord(content, self.roomKeyWords.keys()):
                # self.keyWordJoinRoom(sender, content)
                Thread(target=self.keyWordJoinRoom, args=(sender, content)).start()

            # Ai对话 Ai锁功能 对超管没用
            elif self.aiLock or sender in self.Administrators:
                Thread(target=self.getAiMsg, args=(content, sender)).start()
            # 超级管理员发消息转发给好友
            if judgeSplitAllEqualWord(content, self.sendMsgKeyWords):
                Thread(target=self.sendFriendMsg, args=(content,)).start()
            # 好友消息转发给超级管理员 超级管理员不触发
            if sender not in self.Administrators and self.msgForwardAdmin:
                Thread(target=self.forwardMsgToAdministrators, args=(sender, content)).start()
        
        

    
    def keyWordJoinRoom(self, sender, content):
        """
        关键词进群
        :param sender:
        :param content:
        :return:
        """
        for keyWord in self.roomKeyWords.keys():
            if judgeEqualWord(content, keyWord):
                roomLists = self.roomKeyWords.get(keyWord)
                for roomId in roomLists:
                    roomMember = self.wcf.get_chatroom_members(roomId)
                    if len(roomMember) == 500:
                        continue
                    if sender in roomMember.keys():
                        self.wcf.send_text(f'你小子已经进群了, 还想干吗[旺柴]', receiver=sender)
                        break
                    if self.wcf.invite_chatroom_members(roomId, sender):
                        op(f'[+]: 已将 {sender} 拉入群聊【{roomId}】')
                        break
                    else:
                        op(f'[-]: {sender} 拉入群聊【{roomId}】失败 !!!')

    def sendFriendMsg(self, content):
        """
        给好友发消息 只对超管生效
        :param content:
        :return:
        """
        wxId = content.split(' ')[1]
        sendMsg = f'==== [爱心]来自超管的消息[爱心] ====\n\n{content.split(" ")[-1]}\n\n====== [爱心]NGCBot[爱心] ======'
        self.wcf.send_text(sendMsg, receiver=wxId)

    def getAiMsg(self, content, sender):
        """
        好友Ai对话
        :param content:
        :param sender:
        :return:
        """
        aiMsg = self.Ad.getAi(content)
        if aiMsg:
            
            self.wcf.send_text('本消息由Ai助手生成，不具备法律效益！\n'+aiMsg, receiver=sender)
            return
        self.wcf.send_text(f'Ai对话接口出现错误, 请稍后再试 ~~~', receiver=sender)

    def forwardMsgToAdministrators(self, wxId, content):
        """
        好友消息转发给超级管理员
        :param wxId:
        :param content:
        :return:
        """
        forwardMsg = f"= [爱心]收到来自好友的消息[爱心] =\n好友ID: {wxId}\n好友昵称: {getIdName(self.wcf, wxId)}\n好友消息: {content}\n====== [爱心]NGCBot[爱心] ======"
        for administrator in self.Administrators:
            self.wcf.send_text(forwardMsg, receiver=administrator)


if __name__ == '__main__':
    Fmh = FriendMsgHandle(1)
    Fmh.showWhiteRoom()
