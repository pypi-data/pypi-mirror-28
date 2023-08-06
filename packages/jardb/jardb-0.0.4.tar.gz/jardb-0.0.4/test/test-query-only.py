import sys
sys.path.append("..")
import jardb
import compose
import queue
import storage
import datetime


content = {"Users":[{},[{"Name": "123", "ps": "123"}, {"Name": "1234", "ps": "1234"}]], "Article":[{}, [{"Name": "xxx", "Author": "123"}]], "config": {"user": 1, "secure": 2}}
db = jardb.jardb('json://./database1.db',autosave = False,debug = False)
db.create(content)
db.create_table('Blog',{'id':['AutoIncrease','Unique'],'data':['NotNull','Unique']})
col = db.get_table('Blog')
for i in range(0,10):
    col.add({'data':i,'star':True,'admin':False,'Username':str(i)})

p = db.get_table('Blog')

print(p.value())
print(col.value())
p.filter("$data %3 == 0").remove()
print(p.value())
print(col.value())