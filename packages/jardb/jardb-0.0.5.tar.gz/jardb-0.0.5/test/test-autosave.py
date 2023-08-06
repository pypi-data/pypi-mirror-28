import sys
sys.path.append('..')
import jardb

db = jardb.jardb('file://database.db',autosave = True)
db.create()
db.create_table('Blog')
col = db.get_table('Blog')

for i in range(0,500000):
    col.add({'data':i,'star':True,'admin':False,'Username':str(i)})
