import sys
sys.path.append("..")
import jardb 
import jardb.query

base = jardb.query.BaseQuery('memery')
base.value()
base.remove()
base.add()
base.refresh()

db = jardb.jardb('memery://database.db')
db.create({})
db.create_config('config',{'user':1,'secure':2})
db.show()
q1 = db.get_config('config')
q1.add({'user':5,'data':123})
q1.remove('secure')

q1.has('secure')
q1.has('user')

q1.get('secure')
q1.get('user')
q1.value()
q1.remove('config')

