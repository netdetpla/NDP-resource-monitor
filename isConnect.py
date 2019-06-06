# coding:utf-8
import re
import subprocess

separator = ';'
line = '\n'


def NetCheck(ip):
    try:
        p = subprocess.Popen(["ping -c 10 -w 1 " + ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = str(p.stdout.read())
        # err=p.stderr.read()
        regex = re.compile('100% packet loss')
        # print out
        # print regex
        # print err
        if len(regex.findall(out)) == 0:

            return True
        else:

            return False
    except:
        return 'ERR'


def Update():
    i = 0
    while i < 2:
        flag = NetCheck('114.114.114.114')
        if not flag:
            flag = NetCheck('8.8.8.8')
        else:
            return 'true'
        if not flag:
            pass
        else:
            return 'true'
        i = i + 1
    return 'false'


if __name__ == '__main__':
    NetCheck('114.114.114.114')
    print("hi")
    Update()
    print("hi")
