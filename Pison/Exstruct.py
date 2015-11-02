import _struct as struct

"""
author:kaluluosi
date:2015-11-02

extension of struct lib
surport 
string argument auto encode
variable length string intelligent packing and unpacking,you don't need to set charactor count in fmt

"""

def pack(fmt,*values,encode='utf-8',mode='>'):
    
    #自动编码
    if encode:
        new_values=[]
        for v in values:
            if isinstance(v,str):
                v=v.encode(encode)
            new_values.append(v)
        values = tuple(new_values)

    fmtbdr = [mode,]
    fmt =fmt.replace('x','') #������������x ռλ��
    
    for indx in range(len(fmt)):
        k = fmt[indx]
        if k in ('s', 'p'):
            text = values[indx]
            txtlen = len(text)+1 #�����+1�����ַ�����\x00��β
            fmtbdr += '%ds'%txtlen
        else:
            fmtbdr+=k
    new_fmt = ''.join(fmtbdr)
    return struct.pack(new_fmt,*values)




def unpack(fmt,data,encode='utf-8',mode='>'):

    print("unpack input:",len(data))

    fmt =fmt.replace('x','') #������������x ռλ��
    new_data=bytes()
    fmtbdr =[mode,]
    cursor =0
    
    for k in fmt:
        if k in 'iIlLf':
            cursor+=4
            fmtbdr+=k
        elif k in 'cbB?':
            cursor+=1
            fmtbdr+=k
        elif k in 'hH':
            cursor+=4 if mode=='@'else 2
            fmtbdr+=k
        elif k in 'qQd':
            cursor+=8
            fmtbdr+=k
        elif k in 'P':
            cursor+=4
            fmtbdr+=k
        elif k in 'sp':
            length = 0
            b = data[cursor]
            while b!=0:
                length+=1
                cursor+=1
                b = data[cursor]
            fmtbdr+='%ds'%length
            new_data=data if mode=='@' else data[:cursor]+data[cursor+1:]
    new_fmt = ''.join(fmtbdr)

    values = struct.unpack(new_fmt,new_data)
    #�Զ�����
    if encode:
        new_values=[]
        for v in values:
            if isinstance(v,bytes):
                v=v.decode(encode)
            new_values.append(v)
        values = tuple(new_values)
    return values


def main():
    data =pack('hixcbsi',1,1,'a',1,'hello',0,mode='@')
    print(len(data))
    values = unpack('hixcbsi',data,mode='@')
    

if __name__ == '__main__':
    main()
