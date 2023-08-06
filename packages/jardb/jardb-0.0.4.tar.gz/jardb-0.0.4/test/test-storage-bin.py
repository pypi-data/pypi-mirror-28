import sys
sys.path.append("..")
import compose
import storage
import json

content = {"Users": [{},[{"Name": "李昊", "ps": "123"}, {"Name": "谈健", "ps": "1234"}]], "Article": [{},[{"Name": "xxx", "Author": "123"}]], "config": {"user": 1, "secure": 2}}
db = compose.Dbbase('./database.db')
db.decode(content)

js = storage.BinStroage()

js.write(db)

db1 = js.read('./database.db')

print(db1.encode())