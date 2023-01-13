'''
MongoDB Release3.0
特性：
    1.backuplog.log记录备份日志，workflows.log记录Actions运行日志
    2.借助 pymongo模块 实现数据导出（新增）
    3.默认 clean.cleanSecond ( 15 ) 可自定义保留天数 保留1.0版 clean.cleanFirst([15,30]) 在指定日期清空所有备份记录
'''
import os
import datetime
import sys
import pymongo
import json

# 读入环境变量
MONGODB_URI = os.environ[ 'MONGODB_URI' ]
DB_NAME = os.environ[ 'DB_NAME' ]


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
class cleanComment:
    deleteDays = [ ]

    # def __init__(self):

    def cleanFirst(self, deleteDays):
        '''
        删除旧备份
        方案一，旧版方案，在每月15,30日清除所有json文件
        :param deleteDays: 指定一个删除日期的数组
        :return:
        '''
        self.deleteDays = deleteDays  # 每月15、30号清空备份
        if nowTimeday in deleteDays:
            os.system ( 'rm Comment/*.json -f' )  # 删除所有json
            print ( data + " 清空备份文件" )

    # os.system ( 'rm backuplog.txt.txt -f' )     # 删除日志

    def cleanSecond(self, time):
        '''
        删除旧备份
        方案二，解决方案一的不合理之处，应是最新一天覆盖最旧一天
        :param time: 备份文件保留天数
        :return:
        '''
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


    def get_files(self, path, rule):
        '''
        获取所有json文件
        :param path: 目录
        :param rule: 文件结尾
        :return:
        '''
        all = [ ]
        # fpathe 表示当前访问的文件夹路径
        # dirs 表示当前文件夹下的子文件夹
        # fs 表示当前文件夹下的文件list
        for fpathe, dirs, fs in os.walk ( path ):  # os.walk获取所有的目录
            for f in fs:
                if f.endswith ( rule ):  # 判断结尾
                    all.append ( f )
        return all


# 备份评论数据
class backupComment:
    def __init__(self):
        '''
        连接数据库
        '''
        # Replace the uri string with your MongoDB deployment's connection string.
        conn_str = MONGODB_URI

        # set a 5-second connection timeout
        client = pymongo.MongoClient ( conn_str, serverSelectionTimeoutMS=5000 )
        # db = client.myFirstDatabase  # myFirstDatabase数据库
        # collection = db.comment  # comment表
        db = client[ DB_NAME ]  # myFirstDatabase数据库
        global collection  # comment表
        collection = db[ 'comment' ]
        try:
            client.server_info ()  # 集群信息，如果调用失败说明连接有错误
            print ( data + " 备份成功" )
        except Exception:
            print ( data + " 连接数据库失败，请检查变量MONGODB_URI是否正确" )

    def outputJson(self):
        '''
        保存Json格式的备份文件到Comment目录下
        :return:
        '''
        output = [ ]  # 保存评论数据到列表
        for i in collection.find ():
            output.append ( i )
        # print ( output )
    
        # 创建一个保存备份的目录
        path = os.path.dirname ( __file__ )
        path = path + '/Comment'
        if not os.path.exists ( path ):
            os.mkdir ( path )
            
        jsonPath = 'Comment/' + f'{nowTime.year}年{nowTime.month}月{nowTime.day}日.json'

        '''
        方案一，一行一条数据
        例如：
        	{"id":"001","name":"小张"}
        	{"id":"002","name":"张张"}
        '''
        with open ( jsonPath, 'w', encoding="UTF-8" ) as f:
            for line in output:
                line = json.dumps ( line, ensure_ascii=False )
                f.writelines ( line + '\n' )

        '''
        方案二，标准的JSON格式
        例如：
        	{
        	    "id":"001",
        	    "name":"小张"
        	},
        	{
        	    "id":"002",
        	    "name":"张张"
        	}
        '''
        # with open(jsonPath, 'w', encoding="UTF-8") as jf:
        #     jf.write(json.dumps(output, indent=1))


if __name__ == "__main__":
    sys.stdout = Logger ( "backuplog.log" )  # 输出日志
    print ( "--------------------------------------------------------------\n" )
    nowTime = datetime.datetime.now ()  # 当前时间
    nowTimeday = nowTime.day  # 日
    data = f"{nowTime.year}年{nowTime.month}月{nowTime.day}日"

    '''
    清理备份文件
    '''
    clean = cleanComment ()
    # clean.cleanFirst([15,30])  # 方法一，在每月15,30号清空备份
    clean.cleanSecond ( 15 )  # 方法二，备份保留15天

    '''
    输出当日评论Json文件
    '''
    output = backupComment ()
    output.outputJson ()

    print ()
