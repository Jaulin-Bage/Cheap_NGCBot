from BotServer.BotFunction.RoomMsgFunction import RoomMsgFunction
from BotServer.BotFunction.PointFunction import PointFunction
from BotServer.BotFunction.InterfaceFunction import *
from ApiServer.AiServer.AiDialogue import AiDialogue
from BotServer.BotFunction.JudgeFuncion import *
from DbServer.DbMainServer import DbMainServer
import Config.ConfigServer as Cs
from threading import Thread
import re


class RoomMsgHandle:
    def __init__(self, wcf):
        """
        超级管理员功能 所有功能+管理员操作
        管理员功能 积分功能+娱乐功能
        白名单群聊功能 积分功能免费
        黑名单群聊功能 所有功能无法使用 管理员以及超管除外
        普通群聊功能 所有功能正常使用
        :param wcf:
        """
        self.wcf = wcf
        self.Ad = AiDialogue()
        self.Dms = DbMainServer()
        self.Pf = PointFunction(self.wcf)
        self.Rmf = RoomMsgFunction(self.wcf)
        configData = Cs.returnConfigData()
        self.Administrators = configData['Administrators']
        self.threatBookWords = configData['functionKeyWord']['threatBookWord']
        self.threatBookPoint = configData['pointConfig']['functionPoint']['wbIp']
        self.searchPointKeyWord = configData['pointConfig']['queryPointWord']
        self.aiMsgPoint = configData['pointConfig']['functionPoint']['aiPoint']
        self.aiPicKeyWords = configData['functionKeyWord']['aiPic']
        self.aiPicPoint = configData['pointConfig']['functionPoint']['aiPicPoint']
        self.joinRoomMsg = configData['customMsg']['joinRoomMsg']
        self.joinRoomCardData = configData['customMsg']['JoinRoomCard']
        self.appointJoinRoomMsgs = configData['customMsg']['appointJsonRoomMsgs']
      
    def mainHandle(self, msg):

        # print('消息类型-----------------------------', msg.type)
        # 积分功能
        Thread(target=self.Pf.mainHandle, args=(msg,)).start()
           
        # 入群欢迎
        # Thread(target=self.JoinRoomWelcome, args=(msg,)).start()
        # 推送群聊和白名单群聊才可以使用群聊总结功能&撤回消息检测功能&发言排行榜功能&定时推送总结
        Thread(target=self.Rmf.mainHandle, args=(msg,)).start()
        
       

    def RoomMsgFunction(self, msg):
        """
        群聊消息服务
        :param msg:
        :return:
        """


    def JoinRoomWelcome(self, msg):
        """
        进群欢迎
        :param msg:
        :return:
        """
        pass

    


if __name__ == '__main__':
    configData = Cs.returnConfigData()
    appointJoinRoomMsgs = configData['customMsg']['appointJsonRoomMsgs']
    for ids, msgs in appointJoinRoomMsgs.items():
        print(ids)
