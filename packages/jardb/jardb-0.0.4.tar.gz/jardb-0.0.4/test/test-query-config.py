import sys
sys.path.append("..")
import jardb 

db = jardb.jardb('memery://database.db')
db.create({})
db.create_config('config',{'user':1,'secure':2})
print(db.show())
q1 = db.get_config('config')
print(q1)

q1.add({'user':5,'data':123})
q1.remove('secure')

print(q1.has('secure'))
print(q1.has('user'))

print(q1.get('secure'))
print(q1.get('user'))
print(q1.value())


