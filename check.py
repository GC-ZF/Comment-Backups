"""
@Author:张时贰
@Date:2022年09月20日
@CSDN:张时贰
@Blog:zhangshier.vip
"""
'''
功能：筛选评论
筛选除了user列表中用户的数据
'''
import json

with open ( 'comment.json', encoding='utf-8' ) as f:
    dic = json.load ( f )

user = [ '张时贰', '二花', 'Gmc', '心流', '萌新源', '清云晓晨曦', 'Teacher Du',
         'shaw', 'Sevin', '米耀华', '是非题', '希恩', '一泽', 'vian', '是非题',
         '小梁', '小鲨鱼' ]

length = dic.__len__ ()
print ( length )
# 方法一
# check=[]
# for i in range ( length ):
#     if dic[ i ][ 'nick' ] not in user:
#         check.append(dic[i])

# 方法贰
count = 0
for i in range ( length ):
    if dic[ i - count ][ 'nick' ] in user:
        del dic[ i - count ]
        count = count + 1

with open ( 'check.json', 'w', encoding='utf-8' ) as write_f:
    write_f.write ( json.dumps ( dic, indent=4, ensure_ascii=False ) )
