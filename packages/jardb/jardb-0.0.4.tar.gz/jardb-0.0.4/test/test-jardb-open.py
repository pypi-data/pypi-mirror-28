import sys
sys.path.append("..")
import jardb
import compose
import queue
import storage
import datetime

db = jardb.jardb('json://./database1.db')

t1 = datetime.datetime.now()

db.open()

t2 = datetime.datetime.now()
print(db.get_table('Blog').size())
t3 = datetime.datetime.now()
print((t2 - t1).seconds)
col = db.get_table('Blog')
col.sort('data')
col.add({'data':998,'star':True,'admin':False,'Username':str(998)})
print((t3 - t2).seconds)