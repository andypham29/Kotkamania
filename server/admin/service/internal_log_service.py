from server.admin.repository.intenal_log_dao import InternalLogDao


class InternalLogService:

    def __init__(self, uri=None):
        self.uri = uri

    def initNhlPlayerStatLogTable(self):
        InternalLogDao(self.uri).initNhlPlayerStatLogTable()

    def getNhlPlayerStatLogByDate(self, date):
        try:
            return InternalLogDao(self.uri).getNhlPlayerStatLogByDate(date)
        except Exception as e:
            return None

    def saveNhlPlayerStatLog(self, log):
        try:
            InternalLogDao(self.uri).saveNhlPlayerStatLog(log)
        except Exception as e:
            print(e)
