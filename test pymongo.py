'''
借助 pymongo 读写数据库测试
文档：
    https://pymongo.readthedocs.io/en/stable/tutorial.html Querying for More Than One Document章节有查询方法
中文实例：
    https://blog.csdn.net/xHibiki/article/details/84524645
    https://blog.csdn.net/Java_cola/article/details/121865491
'''
import pymongo

# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb+srv://1310446718:zf632852@cluster0.i7omd.mongodb.net/?retryWrites=true&w=majority"

# set a 5-second connection timeout
client = pymongo.MongoClient ( conn_str, serverSelectionTimeoutMS=5000 )
# db = client.myFirstDatabase  # myFirstDatabase数据库
# collection = db.comment  # comment表
db = client[ 'myFirstDatabase' ]  # myFirstDatabase数据库
collection = db[ 'comment' ]  # comment表

output = [ ]
for i in collection.find ():
    output.append ( i )
print ( output )

# 标准的JSON格式
# with open('images.json', 'w', encoding="UTF-8") as jf:
#     jf.write(json.dumps(output, indent=1))

# 一行一条数据
with open ( 'Comment test.json', 'w', encoding="UTF-8" ) as f:
    for line in output:
        line = str ( line )
        f.writelines ( line + '\n' )
