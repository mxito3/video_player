from config import sql
from pathlib import Path
import os
uploadFloader='./static/upload'
class videoCheck(object):
    """docstring for videoCheck"""

    def __init__(self):
        super(videoCheck, self).__init__()
        self.uploadFloader = '../static/upload'
        self.sql=sql.Sql("localhost",3306,'root','domore0325','videos')

    def checkExists(self):
        self.sql.connect()
        command = 'select * from videoMap'
        result = self.sql.extractSql(command)
        videos = []
        videoIndex = 1
        for item in result:
            videoItem = {}
            videoName = item[0] + ".mp4"

            if self.existSuchViedo(videoName):
                videoItem['path'] = "/static/upload/" + videoName
                videoItem['title'] = item[1]
                videoItem['index'] = videoIndex
                videos.append(videoItem)
                videoIndex += 1
        self.sql.close()
        return videos


    def existSuchViedo(self, name):

        myfile = Path(os.path.abspath(uploadFloader) + "/" + name)
        if myfile.is_file():
            # print("")
            print("存在"+os.path.abspath(uploadFloader) + "/" + name)
            return True;
        else:
            print("不存在"+os.path.abspath(uploadFloader) + "/" + name)
            return False

# class ClassName(object):
#     """docstring for ClassName"""
#     def __init__(self, arg):
#         super(ClassName, self).__init__()
#         self.arg = arg
        