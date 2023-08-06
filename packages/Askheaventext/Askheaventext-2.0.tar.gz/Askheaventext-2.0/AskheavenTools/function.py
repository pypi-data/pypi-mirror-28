# coding:utf-8
__author__="Askheaven"
__date__ = "$2018-1-16 15:07:35$"
#define a function
def InsertToList(listName, stringValue):
    i = 0;
    while 1:
        if i + 2 >= len(listName):
            break
        elif 2 not in listName[i:]:
            # print a[i:]
            break
        i = listName.index(2, i + 1)
        # print a[i:]
        listName.insert(i, stringValue)
        i += 1
    return listName

def UpperFAL(stringname):
    s = ""
    for i in stringname.split(" "):
        s = s + i[:-1].capitalize() + i[-1].upper()
        s = s + " "
    return s

def UpperString(stringname, stringValue):
    s = ""
    for i in stringname:
        if i == stringValue:
            s = s + i.upper()
        else:
            s = s + i
    return s