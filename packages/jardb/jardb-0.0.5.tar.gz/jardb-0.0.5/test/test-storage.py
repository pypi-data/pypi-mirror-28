import sys
sys.path.append('..')
import jardb
import jardb.storage

base = jardb.storage.BaseStorage()
base.write()
base.read()

content = {"Users":[{},[{"Name": "123", "ps": "123"}, {"Name": "1234", "ps": "1234"}]], 
            "Article":[{}, [{"Name": "xxx", "Author": "123"}]], "config": {"user": 1, "secure": 2}}

db1 = jardb.jardb('json://./database1.db',debug = True)
db1.create(content)
db1.save()
db1.open()
db1.close()

db2 = jardb.jardb('file://./database1.db',debug = True)
db2.create(content)
db2.save()
db2.open()

db3 = jardb.jardb('memery://./database1.db',debug = True)
db3.create(content)
db3.save()
db3.open()

