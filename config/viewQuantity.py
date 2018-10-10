from config import sql
import datetime
import time
class viewQuantity(object):
    def __init__(self):
        self.sql=sql.Sql("localhost",3306,'root','domore0325','videos')
        self.sql.connect()
        

    def updateDailyQuantity(self):
        #
        while True:
            needSleepTime=(datetime.datetime.combine(datetime.date.today(), datetime.time.max)-datetime.datetime.now()).total_seconds()
            print("将要休眠"+str(needSleepTime))
            time.sleep(needSleepTime)
            print("休眠完成")
            command='insert into requestQuanitity(quantity,time)values('"'%s'"','"'%s'"')'%(self.getCachedQuantity(),int(time.time()))
            self.sql.extractSql(command)
            self.updateCacheQuantity(type='reset')
        # self.sql.close()

    def getQuantity(self):
        
        command="select * from requestQuanitity"
        result=self.sql.extractSql(command)
        self.sql.close()
        return result

    def getCachedQuantity(self):
       
        command="select * from quantityCache"
        result=self.sql.extractSql(command)
    
        self.sql.close()
        print(result)
        return int(result[0][1])

    def updateCacheQuantity(self,type=None):
        quantity=0
        if type == 'reset':
            print("重置")
            quantity=0
        else:
            quantity=self.getCachedQuantity()+1
        print("缓存将要被为"+str(quantity))

        command='update quantityCache set quantity=%s where id=1'%quantity
        # print(command)
        self.sql.extractSql(command)
        self.sql.close()