# coding=utf-8
from dbutil import db , EMAILADD_COL , WIT_COL 
import random
import smtplib
class MsgGetter(object):
    def get_random_msg(self):
        raise NotImplementedError

class WitMsgGetter(MsgGetter):
    def get_random_msg(self):
        count = db[WIT_COL].find().count()
        val = random.randint(0,count)
        txt = db[WIT_COL].find().limit(-1).skip(val).next()["text"]
        return txt

class EmailAddGetter(object):
    def get_emails(self):
        raise NotImplementedError

class TotalEmailAddRandomGetter(EmailAddGetter):
    def get_emails(self):
        total_count = db[EMAILADD_COL].find().count()

        addrs = []

        for addr in db[EMAILADD_COL].find():
            addrs.append(addr)

        sampling_count = 20#about 20 friends

        adds = []
        for addr in random.sample(addrs , sampling_count):
            print addr["nickname"]
            adds.append(addr["address"])

        return adds

class EmailSender(object):
    def __init__(self):
        self.sender_add = "meaningful.deeds@gmail.com"
        self.password = "xh24206688"
        self.host = "smtp.gmail.com"
        self.port = 587
        
    def send_email(self,msg):
        raise NotImplementedError

class WitGmailSender(EmailSender):
    def __init__(self):
        EmailSender.__init__(self)
        #login to stmp server
        smtpserver = smtplib.SMTP(self.host,self.port)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(self.sender_add, self.password)

        print "login succesfully"
        self.server = smtpserver 


    def preapre_msg(self,wit):
        to_fields = ','.join(self.to_adds)
        header = 'To:' + to_fields + '\n' + 'From: ' + self.sender_add + '\n' + 'Subject:\n'
        begining= u"恭喜你，你被随机了。既来之，则安之，希望下面这句话对你有所启发：\n\n"
        ending = u"\n\n这封邮件来自'all-that-is-meaningful'自动邮件发送robot。\n"
        msg = '\n'.join([header,begining,wit,ending])
        return msg

    def send_email(self,msg):
        msg = self.preapre_msg(msg)
        print "prepare done" 
        print self.to_adds
        self.server.sendmail(self.sender_add, self.to_adds, msg)
        print 'send done!'
        #self.server.close()

    def set_toaddr(self,toadd):
        self.to_adds = [toadd]#it should be a list

class EmailSenderFactory(object):

    def create_email_getter(self):
        raise NotImplementedError

    def create_email_sender(self):
        raise NotImplementedError

    def create_msg_getter(self):
        raise NotImplementedError

    def send_msg(self):
        sender = self.create_email_sender()
        add_getter = self.create_email_getter()
        msg_getter = self.create_msg_getter()

        mail_addrs = add_getter.get_emails()
        for addr in mail_addrs:
            sender.set_toaddr(addr)
            msg = msg_getter.get_random_msg()
            print addr,msg
            sender.send_email(msg)
            print  'sending to %s:\n %s\n' %(addr,msg)

class WitSenderFactory(EmailSenderFactory):
    def create_email_getter(self):
        return TotalEmailAddRandomGetter()

    def create_email_sender(self):
        return WitGmailSender()

    def create_msg_getter(self):
        return WitMsgGetter()

if __name__ == "__main__":
    wsf = WitSenderFactory()
    wsf.send_msg()

