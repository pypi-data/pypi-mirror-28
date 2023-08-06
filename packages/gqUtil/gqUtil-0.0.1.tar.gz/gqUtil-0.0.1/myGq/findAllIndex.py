# coding:utf-8

def find_all_index(uString,target):
    k=[]
    i=-1
    while 1==1:
        i = uString.find(target,i+1)
        if i==-1:
            break
        k.append(i)
    return k