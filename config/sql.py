import pymysql as db
class Sql:
    def __init__(self,host,port,user,passwd,db):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.db=db

    def connect(self):
        self.con=db.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.db)
        self.cursor = self.con.cursor()
    def close(self):
        self.cursor.close()
        self.con.close()
    def extractSql(self,command):
        try:
            cursor.execute(command)
            self.con.commit()
        except:
            self.connect()
            cursor = self.con.cursor()
            cursor.execute(command)
            self.con.commit()
        return cursor.fetchall()

    # def checkCursor():
    #     try:
    #         cursor = self.con.cursor()
    #         cursor.execute(sql)
    #     except:
    #         self.connect()
    #         cursor = self.conn.cursor()
    #         cursor.execute(sql)
    #     return cursor

    # def _ping(self):
    #     try:
    #         if self.con is None:
    #             self.connect()
    #             return True

    #     except db.OperationalError, e:
    #         LOGGER.warn('Cannot connect to mysql - retrying in {} seconds'.format(self.time_to_sleep))
    #         LOGGER.exception(e)
    #         return False        
# test=Sql()    