from pyquery import PyQuery as pq
from codecs import open
from dbutil import db,EMAILADD_COL

doc = pq(open("email.raw.dat").read())

for i in doc.find(".groupclose a"):
    i = pq(i)
    email_add = i.attr("title")
    nickname = i.text()
    db[EMAILADD_COL].save({"address":email_add,"nickname":nickname,})
    print nickname , email_add , "saved"
    
print len(doc.find(".groupclose a"))
