'''
https://blog.csdn.net/weixin_51343683/article/details/120811195
日志测试，设定过期时间，删除备份文件
'''
import datetime
import os


def get_files(path, rule):
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
    timed = 3  # 评论文件过期时间，保留近 timed 天的文件
    comment = get_files ( path='./', rule=".json" )  # 找出所有json文件
    length = comment.__len__ ()

    # 格式化转化为datetime类型
    for i in range ( length ):
        comment[ i ] = comment[ i ].replace ( '.json', '' )
        comment[ i ] = datetime.datetime.strptime ( comment[ i ], "%Y年%m月%d日" ).date ()  # 格式化202?-??-??

    nowTime = datetime.datetime.now ()  # 获取当前时间
    overTime = (nowTime + datetime.timedelta ( days=-timed )).date ()  # 获取过期时间 .date()只要日期
    # print ( "获取过期时间:", overTime )

    for i in comment:
        if (overTime >= i):
            print ( f"{i.year}年{i.month}月{i.day + 1}日" )
            shell = 'rm ' + f"{i.year}年{i.month}月{i.day + 1}日" + '.json'
            code = os.system ( shell )
