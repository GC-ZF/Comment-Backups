'''
旧版方案已不适用
MongoDB Release1.0
特性：
    1.backuplog.log记录备份日志，workflows.log记录Actions运行日志
    2.借助官方工具 mongoimport.exe 实现数据导出
    3.delete_day = [ 15, 30 ]   每月15、30号清空所有Json文件
'''
import os
from datetime import datetime
import sys

# 读入环境变量
MONGODB_URI = os.environ[ 'MONGODB_URI' ]


class Logger ( object ):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open ( fileN, "a" )

    def write(self, message):
        self.terminal.write ( message )
        self.log.write ( message )

    def flush(self):
        pass


sys.stdout = Logger ( "backuplog.log" )  # 输出日志
print ( "--------------------------------------------------------------\n" )
now_time = datetime.now ()  # 当前时间
now_time_day = now_time.day  # 日
data = f"{now_time.year}年{now_time.month}月{now_time.day}日"
delete_day = [ 15, 30 ]  # 每月15、30号清空备份
if now_time_day in delete_day:
    os.system ( 'rm *.json -f' )  # 删除所有json
    print ( data + " 清空备份文件" )
    # os.system ( 'rm backuplog.txt.txt -f' )     # 删除日志
# MONGODB_URI = input('输入MONGODB_URI')
commond = 'mongoexport --uri ' + f'{MONGODB_URI}' + ' --collection comment --forceTableScan --type json --out Comment/' + f"{now_time.year}年{now_time.month}月{now_time.day}日.json"
code = os.system ( commond )
if code == 0:
    print ( data + " 备份成功" )
else:
    print ( data + " 备份失败，请检查python文件中MONGODB_URI值是否正确" )
print ()
