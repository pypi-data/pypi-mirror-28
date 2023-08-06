import sys
sys.path.append("..")
import jardb
import datetime

content = {"Users":[{},[{"Name": "123", "ps": "123"}, {"Name": "1234", "ps": "1234"}]], "Article":[{}, [{"Name": "xxx", "Author": "123"}]], "config": {"user": 1, "secure": 2}}
db = jardb.jardb('json://./database1.db',autosave = False,debug = True)

db.create(content)

db.create_table('Blog',{'id':['AutoIncrease','Unique'],'data':['NotNull','Unique']})
col = db.get_table('Blog')

t1 = datetime.datetime.now()

for i in range(0,10):
    col.add({'data':i,'star':True,'admin':False,'Username':str(i)})

t2 = datetime.datetime.now()
col.filter("$data %3 == 0").remove()
t3 = datetime.datetime.now()
col.update({'star':False,'ad':True})
t4 = datetime.datetime.now()

# print(col.filter("$data % 4 == 0").value())
db.remove('Users')
db.remove('config')
db.remove('Blog')
print(col)
print(db.show())
t5 = datetime.datetime.now()
t6 = datetime.datetime.now()
print((t2 - t1).seconds)
print((t3 - t2).seconds)
print((t4 - t3).seconds)
print((t5 - t4).seconds)
print((t6 - t5).seconds)