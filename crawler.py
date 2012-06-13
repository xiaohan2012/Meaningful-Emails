# coding=utf-8
import weibo2 as wb2
from dbutil import db , CONFIG_COL , WIT_COL
from pprint import pprint

class Crawler(object):

    def fetch_wits(self):
        raise NotImplementedError

    def save_wits(self):
        raise NotImplementedError

class WeiboCrawler(Crawler):
    uname_lst = [u"书籍里的小阳光"]
    uid_lst = []
    APP_KEY = "3945826067"
    APP_SECRET = "9ad09b3f99da46fb8a0aa897b619358f"
    ACCESS_TOKEN = "2.00klTSNCvbRC_E7b58287363mZ1YhD"
    EXPIRES_IN = 1349309377
    
    def __init__(self):
        self.cli = wb2.APIClient(WeiboCrawler.APP_KEY ,WeiboCrawler.APP_SECRET , redirect_uri = "http://vedaclub.org/" )
        self.cli.set_access_token(WeiboCrawler.ACCESS_TOKEN , WeiboCrawler.EXPIRES_IN)
        self.config_key = "weibo_crawler"

    def fetch_wits(self):
        for uname in WeiboCrawler.uname_lst:
            page = 1
            since_id = self.get_since_id()
            while True:
                ret = self.cli.get.statuses__user_timeline(screen_name = uname ,page = page , count = 50)
                print "\npage %d\n" %(page)
                page += 1
                if ret["statuses"]:
                    for s in ret["statuses"]:
                        wit = s["text"]
                        wit_obj = {
                            "text":wit,
                            "from":"weibo",
                            "uname":uname
                        }
                        self.save_wit(wit_obj)
                        print "wit %s saved" %wit


                        if since_id < s["id"]:
                            since_id = s["id"]
                            print "new since_id",since_id

                    self.save_since_id(since_id)                        
                else:
                    break
    def get_since_id(self): 
        try:
            return db[CONFIG_COL].find_one({"key":"since_id","type":self.config_key})["value"]
        except TypeError:
            return 0

    def save_since_id(self,new_id):
        db[CONFIG_COL].update({"key":"since_id" , "type":self.config_key},{"$set":{"value":new_id } } , True)

    def save_wit(self,wit_obj):
        db[WIT_COL].save(wit_obj)

class CrawlerFactory(object):

    def create_crawler(self):
        raise NotImplementedError("it is a factory method")

    def crawl(self):
        self.crawler.fetch_wits()


class SnsCrawlerFactory(CrawlerFactory):

    def create_crawler(self,sns_type= "weibo"):
        d_ = {
            "weibo":WeiboCrawler
        }
        self.crawler = d_[sns_type]()

if __name__ == "__main__":
    factory = SnsCrawlerFactory()
    factory.create_crawler("weibo")
    factory.crawl()

