import sys
sys.path.append("..")
import jardb.compose as compose
import json

base = compose.DbBaseObject()
base.encode()
base.decode()
base.get()

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

assert rd1.get() == {'Name':'123','ps':'123'}
rd1.set_('ps','12345')
assert rd1.encode() == {'Name':'123','ps':'12345'}
rd1.reset({'Name':'123','ps':'123'})
assert rd1.find('Name') == '123'
assert rd1.find('id') == None

table1.get()
table1.encode()
table1.set_child_list([rd1,rd2,rd3])
assert table1.size() == 3

assert conf.get() == {'user':1,'secure':2}
conf.set_content({'a':1,'b':2})

db.encode()
db.get()

assert db.find('config') != None
db.remove('config')
assert db.find('config') == None


db.decode({"Users":[{},[{"Name": "123", "ps": "123"}, {"Name": "1234", "ps": "1234"}]], "Article":[{}, [{"Name": "xxx", "Author": "123"}]], "config": {"user": 1, "secure": 2}})
try:
    db.decode({'123':'123'})
except:
    pass