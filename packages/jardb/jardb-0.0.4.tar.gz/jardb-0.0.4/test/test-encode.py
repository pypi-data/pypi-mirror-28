import sys
sys.path.append("..")
import compose
import json

db = compose.Dbbase('Menery')
table1 = compose.DbTable('Users')
table2 = compose.DbTable('Article')
db.insert(table1)
db.insert(table2)
rd1 = compose.DbRecord({'Name':'123','ps':'123'})
table1.insert(rd1)
rd2 = compose.DbRecord({'Name':'1234','ps':'1234'})
table1.insert(rd2)
rd3= compose.DbRecord({'Name':"xxx",'Author':'123'})
table2.insert(rd3)

conf = compose.DbConfig('config',{'user':1,'secure':2})
db.insert(conf)

strs = db.encode()

print(strs)
print(json.dumps(strs))
