﻿# 将dict对象格式化输出成字符串
"""
author:kaluluosi
date:2015-11-02

dump pyton object to string and format it.

"""

_lines = []
indent=4

def tab(depth=0):
    return ' '*indent*depth

def toStr(s):
    return "\"%s\""%s

def islambda(s):
    return 'lambda' in s

def writeline():
    _lines.append('\n')

def parse(obj,depth=0):
    if isinstance(obj,str):
        if islambda(obj):
            _lines.append(obj)
        else:
            _lines.append(toStr(obj))
    else:
        if isinstance(obj,dict):
            parse_dict(obj,depth)
        elif isinstance(obj,list):
            parse_list(obj,depth)
        else:
            _lines.append(str(obj))

def parse_dict(dic,depth=0):
    _lines.append('{') #开头
    writeline() #换行
    depth+=1 #缩进增加
    
    #循环遍历所有的item
    for k,v in dic.items():
        _lines.append(tab(depth)) #缩进
        parse(k,depth) #
        _lines.append(':')
        parse(v,depth) #值
        _lines.append(',')
        writeline() #换行

    depth-=1 #缩进还原
    _lines.append(tab(depth)+'}') #结束

def parse_list(lst,depth=0):
    _lines.append('[') #开头
    writeline() #换行
    depth+=1 #缩进增加
    
    #循环遍历所有的item
    for v in lst:
        _lines.append(tab(depth))
        parse(v,depth)
        _lines.append(',')
        writeline() #换行

    depth-=1 #缩进还原
    _lines.append(tab(depth)+']') #结束

def dumps(obj,indent=True):
    parse(obj)
    c=''
    if indent:
        c = ''.join(_lines)
    else:
        c = ''.join([l.strip() for l in _lines])
    return c



def main():
    dic = { 'a':1,1:'2',2:{1:1,2:2},3:[1,2,4,5,6,7],4:"lambda :print('a')"}
    c = dumps(dic,False)
    print(c)
    
if __name__ == '__main__':
    main()

