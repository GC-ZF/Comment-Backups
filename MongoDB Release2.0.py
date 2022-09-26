'''
旧版方案已不适用
MongoDB Release2.0
特性：
    1.backuplog.log记录备份日志，workflows.log记录Actions运行日志
    2.借助官方工具 mongoimport.exe 实现数据导出
    3.默认 clean.cleanSecond ( 15 ) 可自定义保留天数 保留1.0版 clean.cleanFirst([15,30]) 在指定日期清空所有备份记录（新增）
'''
import os
import datetime
import sys

# 读入环境变量
MONGODB_URI = os.environ[ 'MONGODB_URI' ]


# 打印日志
class Logger ( object ):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open ( fileN, "a" )

    def write(self, message):
        self.terminal.write ( message )
        self.log.write ( message )

    def flush(self):
        pass


# 清理备份文件
class backupComment:
    deleteDays = [ ]

    # def __init__(self):

    '''
    删除旧备份
    方案一，旧版方案，在每月15,30日清除所有json文件
    '''

    def cleanFirst(self, deleteDays):
        self.deleteDays = deleteDays  # 每月15、30号清空备份
        if nowTimeday in deleteDays:
            os.system ( 'rm Comment/*.json -f' )  # 删除所有json
            print ( data + " 清空备份文件" )

    # os.system ( 'rm backuplog.txt.txt -f' )     # 删除日志

    '''
    删除旧备份
    方案二，解决方案一的不合理之处，应是最新一天覆盖最旧一天
    '''

    def cleanSecond(self, time):
        self.timed = time  # 评论文件过期时间，保留近 timed 天的文件
        comment = self.get_files ( path='./', rule=".json" )  # 找出所有json文件
        length = comment.__len__ ()

        # 格式化转化为datetime类型
        for i in range ( length ):
            comment[ i ] = comment[ i ].replace ( '.json', '' )
            comment[ i ] = datetime.datetime.strptime ( comment[ i ], "%Y年%m月%d日" ).date ()  # 格式化为202?-??-??

        nowTime = datetime.datetime.now ()  # 获取当前时间
        overTime = (nowTime + datetime.timedelta ( days=-self.timed )).date ()  # 获取过期时间 .date()只要日期 ??-??
        # print ( "获取过期时间:", overTime )

        # 遍历依次删除过期备份
        for i in comment:
            if (overTime >= i):
                print ( '删除' + f"{i.year}年{i.month}月{i.day}日" + '.json' )
                shell = 'rm Comment/' + f"{i.year}年{i.month}月{i.day}日" + '.json'
                code = os.system ( shell )

    '''
    获取所有json文件
    '''

    def get_files(self, path, rule):
        all = [ ]
        # fpathe 表示当前访问的文件夹路径
        # dirs 表示当前文件夹下的子文件夹
        # fs 表示当前文件夹下的文件list
        for fpathe, dirs, fs in os.walk ( path ):  # os.walk获取所有的目录
            for f in fs:
                if f.endswith ( rule ):  # 判断结尾
                    all.append ( f )
        return all


if __name__ == "__main__":
    sys.stdout = Logger ( "backuplog.log" )  # 输出日志
    print ( "--------------------------------------------------------------\n" )
    nowTime = datetime.datetime.now ()  # 当前时间
    nowTimeday = nowTime.day  # 日
    data = f"{nowTime.year}年{nowTime.month}月{nowTime.day}日"

    clean = backupComment ()
    # clean.cleanFirst([15,30])  # 在每月15,30号清空备份
    clean.cleanSecond ( 15 )  # 备份保留15天
    # MONGODB_URI = input('输入MONGODB_URI')
    commond = 'mongoexport --uri ' + f'{MONGODB_URI}' + ' --collection comment --forceTableScan --type json --out Comment/' + f"{nowTime.year}年{nowTime.month}月{nowTime.day}日.json"
    code = os.system ( commond )
    if code == 0:
        print ( data + " 备份成功" )
    else:
        print ( data + " 备份失败，请检查python文件中MONGODB_URI值是否正确" )
    print ()
