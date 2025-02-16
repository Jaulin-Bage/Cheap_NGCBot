from DbServer.DbRoomMsgServer import DbRoomMsgServer
from DbServer.DbPointServer import DbPointServer
from DbServer.DbUserServer import DbUserServer
from DbServer.DbRoomServer import DbRoomServer
from DbServer.DbSignServer import DbSignServer
from DbServer.DbInitServer import DbInitServer
from DbServer.DbGhServer import DbGhServer
import Config.ConfigServer as Cs
from OutPut.outPut import op


class DbMainServer:
    def __init__(self):
        self.Dps = DbPointServer()
        self.Dus = DbUserServer()
        self.Drs = DbRoomServer()
        self.Dss = DbSignServer()
        self.Dis = DbInitServer()
        self.Dgs = DbGhServer()
        self.Dms = DbRoomMsgServer()
        self.configData = Cs.returnConfigData()




    