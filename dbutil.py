import pymongo
class DB(pymongo.database.Database):
    conn = pymongo.Connection()
    def __init__(self):
        pymongo.database.Database.__init__(self,DB.conn,"inspirator")
    
CONFIG_COL = "config"
WIT_COL = "wit"
EMAILADD_COL = "email_add"

db = DB()

#ensure index part
db[CONFIG_COL].ensure_index([("key",pymongo.ASCENDING),("type",pymongo.ASCENDING)])
db[WIT_COL].ensure_index([("text",pymongo.ASCENDING)],unique = True)
db[EMAILADD_COL].ensure_index([("address",pymongo.ASCENDING)],unique = True)
