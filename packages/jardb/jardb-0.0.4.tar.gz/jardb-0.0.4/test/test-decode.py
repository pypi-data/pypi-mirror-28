import sys
sys.path.append("..")
import compose

content = {"Users": [{"Name": "123", "ps": "123"}, {"Name": "1234", "ps": "1234"}], "Article": [{"Name": "xxx", "Author": "123"}], "config": {"user": 1, "secure": 2}}

db = compose.Dbbase('Menery')

db.decode(content)

str = db.encode()
print(str)