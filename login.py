# -*- coding: utf-8 -*-

import urllib3
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import time


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def alert_admin(content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = _format_addr(u'卞学胜 <%s>' % from_addr)
    message['To'] = _format_addr(u'同学 <%s>' % u'卞学胜')
    subject = u'厦门大学低电量警报'  # 主题
    message['Subject'] = Header(subject, 'utf-8')
    server.sendmail(from_addr, ['541435721@qq.com'], message.as_string())


from_addr = 'wow00ms@126.com'
password = "bym821121"
smtp_server = 'smtp.126.com'

try:
    server = smtplib.SMTP(smtp_server, 25)
    flag = server.login(from_addr, password)
    print "login success", flag
except smtplib.SMTPException, e:
    print "Error: cannot send email"
    print(e)
    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)

no = [
    #  '宿舍码', '楼栋号', '房间号',姓名,邮箱,警告值
    ['05', '07', '0607', u'卞学胜', '541435721@qq.com', 10],
    ['05', '07', '0908', u'伟权', '472483520@qq.com', 10],
    ['04', '09', '0606', u'老张', 'handsomeshanxin@163.com', 15],
    ['04', '06', '0622', u'渭哥', 'weili_xs@163.com', 10],
    ['04', '09', '0509', u'大师兄', 'david102812@gmail.com', 10],

]

getCode_url = "http://ecardservice.xmu.edu.cn:81/Account/SignIn"
home_url = 'http://ecardservice.xmu.edu.cn/'
get_cost_url = 'http://ecardservice.xmu.edu.cn/AutoPay/PowerFee/GetPowerBalance'
header = {
    "User-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    "Cookie": "_ga=GA1.3.289855958.1515385233; ASP.NET_SessionId=twvfa1lndbbh5bm5wfpf35dh; iPlanetDirectoryPro=VUlBU18yMzAyMDE3MDE1NTUyN18yMDE4MDExMTE5NDg1Nzg2NDY%3d"
}
# header['Host']="icp.alexa.cn"
# header['User-Agent']="Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
# header['Cache-Control'] = "max-age=0"
http = urllib3.PoolManager()

# res = http.request('POST', getCode_url, headers=header)
# res1 = http.request('POST', home_url, headers=header)
timer = 0
counter = [0, ]  # 网站查询异常次数
while (True):
    flag = False
    count = 0
    for record in no:
        count += 1
        fields = {
            u"payTypeCode": u"PowerFeeSims",
            u"xiaoqu": unicode(record[0]),
            u"buildno": unicode(record[1]),
            u"roomno": unicode(record[2]),
        }
        remained = http.request('POST', get_cost_url, headers=header, fields=fields)
        receivers = [record[4]]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        degree = remained.data
        try:
            float(degree)
        except Exception, e:
            print('网站查询异常')
            counter[0] += 1
            if counter[0]>10:
                "网站查询异常次数过多！！！！"
            time.sleep(100)
            continue
        counter[0] = 0
        content = u'{0},你的剩余电费为：{1}。\n请尽快充值！！！'.format(record[3], unicode(degree))
        print(count, degree)
        try:
            message = MIMEText(content, 'plain', 'utf-8')
            message['From'] = _format_addr(u'卞学胜 <%s>' % from_addr)
            message['To'] = _format_addr(u'同学 <%s>' % record[3])
            subject = u'厦门大学低电量警报'  # 主题
            message['Subject'] = Header(subject, 'utf-8')
        except Exception, e:
            degree = 1000000  # 防止发送邮件
            print 'encode err', remained.data
            # print fields
            print(e)
            alert_admin("电费监控程序出错,尽快重启！！！！")
            flag = True
            break
        try:
            degree = float(degree)
            if degree < record[5]:
                server.sendmail(from_addr, receivers, message.as_string())
                print "send email successfully"
            else:
                print "regular"
        except smtplib.SMTPException, e:
            print "Error:cannot send email"
            print(e)
        print('----------------')
        time.sleep(2)
    if flag:
        break
    time.sleep(5)
server.quit()

'''
宿舍区代码：
01 本部芙蓉区
02 本部石井区
03 本部南光区
04 本部凌云区
05 本部勤业区
06 本部海滨新区
07 本部丰庭区
26 漳州校区芙蓉园
08 海韵学生公寓
09 曾厝安学生公寓
21 漳州校区博学园
22 漳州校区囊萤园
23 漳州校区笃行园
24 漳州校区映雪园
25 漳州校区勤业园
27 漳州校区若谷园
28 漳州校区凌云园
29 漳州校区丰庭园
30 漳州校区南安园
31 漳州校区南光园
32 漳州校区嘉庚若谷园
33 翔安校区芙蓉区
34 翔安校区南安区
35 翔安校区南光区
42 翔安国光区
41 翔安丰庭区
40 翔安笃行区
10 思明校区留学生区
11 翔安三期H区
12 翔安三期K区
50 翔安校区博学区
51 翔安校区凌云区
52 翔安校区映雪区




'''

# print(res1.data)
