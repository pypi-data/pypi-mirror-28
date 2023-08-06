import sys
sys.path.append("..")
import compose
import query

db = compose.Dbbase('Menery')
table1 = compose.DbTable('Users',{'Name':['NotNull','Unique'],'ps':['AutoIncrease']})
db.insert(table1)

rd1 = compose.DbRecord({'Name':'123','ps':999123})
rd2 = compose.DbRecord({'Name':'1234','ps':1234})
rd3 = compose.DbRecord({'Name':'ad','ps':6664})
table1.insert(rd1)
table1.insert(rd2)
table1.insert(rd3)

a = query.TableQuery(table1)

print(a.find({'Name':'123','ps':123}).value())
print(a.size())
b = query.TableQuery(table1)

print(b.filter("$Name == '123'").value())
print(b.size())

c = query.TableQuery(table1)
print(c.sort('ps',res = True).value())
print(c.get(1).remove())

print(query.TableQuery(table1).value())

d = query.TableQuery(table1)

# print(d.update({'Name':'ertuil','luck':True}).value())

d.add({'Name':"1233"})
d.add({'Name':"1255"})
print(d.add({'Name':"1256"}).sort('ps').get(4).value())
print(db.encode())