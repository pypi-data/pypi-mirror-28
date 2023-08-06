import sys
sys.path.append("..")
import jardb
from jardb.errors import *

content = {"Users":[{},[{"Name": "123", "ps": "123"}, {"Name": "1234", "ps": "1234"}]], "Article":[{}, [{"Name": "xxx", "Author": "123"}]], "config": {"user": 1, "secure": 2}}
db = jardb.jardb('json://./database1.db',autosave = True,debug = True)

db.create(content)

db.create_table('Blog',{'id':['AutoIncrease','Unique'],'data':['NotNull','Unique']})
col = db.get_table('Blog')


for i in range(0,100):
    col.add({'data':i,'star':True,'admin':False,'Username':str(i)})

col.filter("$data % 3 == 0").remove()

col.update({'star':False,'ad':True})
col.filter("$data % 4 == 0").value()
col.find({'star':False}).get(10).sort('id').map('id')
col.refresh()

try:
    col.filter([1,2,3])
except Exception:
    pass
col.size()
col.refresh()
col.add({'data':13})
col.add({'id':1000})
col.update({'data':1}) 
db.remove('Users')
db.remove('config')
db.remove('Blog')
db.show()

db.backup('database2.db')