import sys
sys.path.append("..")
import compose
import storage
import json

content = {"Users": [{},[{"Name": "李昊", "ps": "123"}, {"Name": "谈健", "ps": "1234"}]], "Article": [{},[{"Name": "xxx", "Author": "123"}]], "config": {"user": 1, "secure": 2}}
db = compose.Dbbase('Memery')

db.decode(content)

js = storage.MemeryStroage()
js.write(db)
db1 = js.read()
print(db1.encode())


