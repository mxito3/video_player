import os
import time
import datetime
import uuid
import _thread
import threading
from flask import Flask,render_template,url_for,request,redirect,flash,request,session,make_response
from werkzeug.utils import secure_filename
from config.sql import Sql
from config.viewQuantity import viewQuantity
from config.videoCheck import videoCheck
from pathlib import Path

app=Flask(__name__)
app.secret_key=bytes(str(uuid.uuid4()),'utf-8')
uploadFloader='./static/upload'
app.config['UPLOAD_FLODER']=uploadFloader


sql=Sql("localhost",3306,'root','domore0325','videos')
# 访问量
viewCalculator=viewQuantity()
videoCheck=videoCheck()


@app.route('/')
def videoList():
    viewCalculator.updateCacheQuantity()
    videos=videoCheck.checkExists()
    return render_template('videoList.html',videos=videos)

@app.route('/play')
def root():
    #return url_for('static',filename='js/index.css')
    viewCalculator.updateCacheQuantity()
    videos=videoCheck.checkExists()
    return render_template('index.html',videos=videos)

@app.route('/admin')
def admin():
    user_name=request.cookies.get('username')
    print("cookie  "+user_name)
    if 'admin' != user_name:
        return redirect('/login')
    viewCalculator.updateCacheQuantity()
    quantityMes=[]
    perMes={}
    for item in viewCalculator.getQuantity():
        # time.localtime(item[0])
        # print(item[0])
        # seconds=time.time()
        # print(seconds)
        # updateTime=time.strftime("%Y-%m-%d %H:%M:%S",seconds) 
        updateTime=time.strftime("%Y-%m-%d", time.gmtime(item[1]))
        perMes={}
        perMes['time']=updateTime
        perMes['quantity']=item[0]
        quantityMes.append(perMes)
    todayQuantity=viewCalculator.getCachedQuantity()
    print(todayQuantity)
    # perMes={}
    # perMes.append(todayQuantity)        
    return render_template('admin.html',quantityMes=quantityMes,todayQuantity=todayQuantity)


@app.route('/upload',methods=['Post'])
def file_upload():
    viewCalculator.updateCacheQuantity()
    if 'admin' == request.cookies.get('username'):
        file=request.files['test']
        title=request.form.get('title')
        print(title)
        rawFileName=file.filename
        if title=="" or rawFileName=="":
            mes="未填标题或未选择文件,请重新上传"
        else:
                fileId=str(uuid.uuid4())
                fileName=fileId+".mp4"
                if not os.path.isdir(os.path.abspath(app.config['UPLOAD_FLODER'])):
                    os.mkdir(os.path.abspath(app.config['UPLOAD_FLODER']))
                file.save(os.path.join(app.config['UPLOAD_FLODER'],fileName))
                sql.connect()
                command='insert into videoMap(id,title)values('"'%s'"','"'%s'"')'%(fileId,title)
                print(command)
                sql.extractSql(command)
                sql.close()
                mes="upload file '"+rawFileName +"' with success"
        return mes
    else:
        return "cookie with error"

        


@app.route('/login',methods=['Post','GET'])
def signIn():
    viewCalculator.updateCacheQuantity()
    if request.method == 'POST':
        form=request.form
        user_name=form.get('user_name')
        user_password=form.get('user_password')
        print(user_name)
        print(user_password)
        if user_name == 'admin' and user_password =='123456':
            response=make_response(redirect('/admin'))
            response.set_cookie('username','admin')
            return response
        else:
            flash("用户名密码不匹配")
            return render_template('login.html')
    else:
        return render_template('login.html')




class myThread (threading.Thread):   #继承父类threading.Thread
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        viewCalculator.updateDailyQuantity()
    



if __name__=="__main__":
    # viewCalculator.
    # todayQuantity=viewCalculator.getCachedQuantity()
    # print(todayQuantity)
    # 创建新线程
    thread1 = myThread()
    thread1.start()
    app.run(host='0.0.0.0',threaded=True,port=8080)
# thread2.start()
    # if beforeStart():
    #     
    # else:
    #     print("启动访问量监测线程失败")


