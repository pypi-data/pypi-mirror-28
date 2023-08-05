import os
import configparser
from math import ceil
import re


def toBatchList(keylist, chunked=1):
    length = len(keylist)
    batch_size = ceil(length / chunked)
    n = 1
    while length > batch_size:
        length -= batch_size
        n += 1
    batchKeyWordList = []
    for i in range(1, n + 1):
        if i == 1:
            batch = keylist[i - 1:i * batch_size]
            batchKeyWordList.append(batch.copy())
        else:
            batch = keylist[(i - 1) * batch_size:i * batch_size]
            batchKeyWordList.append(batch.copy())
    return batchKeyWordList


def find_path(toList):
    storage_path = os.path.dirname(os.path.dirname(__file__))+'/'
    response = storage_path
    if type(toList) == str:toList = str(toList).split('_')
    for i in toList:
        response += '{}/'.format(i)
    return response


def get_config(conf_path=''):
    cf = configparser.ConfigParser()
    if conf_path == '':
        config_path = os.path.dirname(os.path.dirname(__file__))+'/conf'
        cf.read(config_path + "/git.ini", encoding='utf-8')
    else:
        cf.read(conf_path, encoding='utf-8')

    sectionsDicts = {}
    for section in cf.sections():
        temp = {}
        for x,y in cf.items(section):
            temp[x] = y
        sectionsDicts[section] = temp

    return sectionsDicts


def type_limit(*typeLimit,**returnType):
    def value_type(func):
        def wrapper(*param,**kw):
            length = len(typeLimit)
            if length != len(param):
                raise IOError("The list of typeLimit and param must have the same length")
            for index in range(length):
                t = typeLimit[index]
                p = param[index]
                if not isinstance(p,t):
                    raise IOError("The param %s should be %s,but it's %s now!"%(str(p),type(t()),type(p)))
            res = func(*param,**kw)
            if "returnType" in returnType:
                limit = returnType["returnType"]
                if  not isinstance(res,limit):
                    raise IOError("This function must return a value that is %s,but now it's %s"%(limit,type(res) ) )
            return res
        return wrapper
    return value_type


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    return round(fsize, 2)


def get_FILE_POSITIONS(sub_store,partitions):
    # 文件名对应索引
    def get_file_index(string):
        return int(re.findall("\[(.*?)\]",string)[0])
    if isinstance(partitions,list) and isinstance(sub_store,dict):
        return {part:sub_store[get_file_index(str(part))] for part in partitions}
    else:
        raise TypeError('{} must be list and {} must be dict.'.format(partitions,sub_store))


def remove_reindex(reindex,key):
    """
    返回删除key后的REINDEX
    :param reindex: 
    :param key: 
    :return: 
    """
    for k,v in reindex.items():
        if key in v:
            v.remove(key)
            reindex[k] = v
    return reindex
