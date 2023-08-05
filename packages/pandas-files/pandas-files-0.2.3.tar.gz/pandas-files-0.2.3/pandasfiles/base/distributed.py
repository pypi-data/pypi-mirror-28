# coding:utf-8
import os
import re
import joblib
from pandasfiles.base.craft import Craft
from pandasfiles.base.template import STORE_NAME,PARTITION_VARIABLE,FILE_KEYS_LIST,INDEX_FILE
from pandasfiles.utils.lylogger import tolog
from pandasfiles.utils.tools import get_FILE_POSITIONS,remove_reindex



class Distribution:


    def __init__(self,partition_name,chunk,mode,index_path,sub_store,log_file_path,silent,primary_key):

        self.__partition_name = partition_name
        self.__chunk = chunk
        self.__mode = mode
        self.__index_path = index_path
        self.__sub_store = sub_store
        self.__logger = tolog(operate_name='distributed', log_file_path=log_file_path,silent=silent)
        self.__primary_key = primary_key

        if mode in ['a','r']:
            try:
                json = joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))
                self.__RE_CHUNKED_INDEXS = json['reindex']
                self.__CHUNKED_INDEXS = json['index']
                self.__KEYS = json['keys']
                self.__partitions = json['partitions']
                self.__FILE_POSITIONS = json['position']
            except:
                raise IOError('Please set current mode if you have operation before.')
        elif mode == 'w':
            self.__RE_CHUNKED_INDEXS = {}
            self.__CHUNKED_INDEXS = {}
            self.__KEYS = []
            self.__partitions = []
            self.__FILE_POSITIONS = {}

        else:
            raise ValueError("mode only can set 'a' , 'w' ,'r'.")

    # 计算对应子结点下的keys数量
    def _check_keys_count(self,is_sorted=True,mode='w'):
        dCounts = {}
        if mode == 'w':
            for i in range(0,self.__chunk):
                s_name = STORE_NAME.format(self.__partition_name,i)
                if s_name in self.__RE_CHUNKED_INDEXS.keys():
                    dCounts[s_name] = len(self.__RE_CHUNKED_INDEXS[s_name])
                else:
                    dCounts[s_name] = 0
        elif mode in ['a','r']:
            dCounts = {k:len(v) for k,v in self.__RE_CHUNKED_INDEXS.items()}

        if is_sorted == False:
            return dCounts
        else:
            return sorted(dCounts.items(), key=lambda x: x[1], reverse=True)


    # 文件名对应索引
    def _get_file_index(self,string):
        return int(re.findall("\[(.*?)\]",string)[0])


    def start(self):
        if self.__mode == 'w':
            for chunk_i in  range(0,self.__chunk):
                s_name = STORE_NAME.format(self.__partition_name,chunk_i)
                globals()[PARTITION_VARIABLE.format(chunk_i)] = Craft(mode='w',
                                                                      store_path=self.__sub_store[chunk_i],
                                                                      store_name=s_name)
                globals()[FILE_KEYS_LIST.format(chunk_i)] =[]
                globals()[PARTITION_VARIABLE.format(chunk_i)].start()
                # 位置信息
                self.__FILE_POSITIONS[s_name] = self.__sub_store[chunk_i]

        elif self.__mode in ['a','r']:
            for s_name in self.__partitions:
                chunk_i = self._get_file_index(s_name)
                globals()[PARTITION_VARIABLE.format(chunk_i)] = Craft(mode=self.__mode,
                                                                      store_path=self.__sub_store[chunk_i],
                                                                      store_name=s_name)
                globals()[FILE_KEYS_LIST.format(chunk_i)] = self.__RE_CHUNKED_INDEXS[s_name]
                globals()[PARTITION_VARIABLE.format(chunk_i)].start()
                # 位置信息
                self.__FILE_POSITIONS[s_name] = self.__sub_store[chunk_i]



    def write(self,key,value):

        if self.__mode == 'w':
            if value.empty is False:
                keyCounts = self._check_keys_count(mode='w')
                fileIndex = self._get_file_index(keyCounts[-1][0])
                globals()[PARTITION_VARIABLE.format(fileIndex)].write(key,value)
                globals()[FILE_KEYS_LIST.format(fileIndex)].append(key)
                self.__KEYS.append(key)
                s_name = STORE_NAME.format(self.__partition_name, fileIndex)
                self.__RE_CHUNKED_INDEXS[s_name] = globals()[FILE_KEYS_LIST.format(fileIndex)]
                if len(value) != 0 : self.__logger.printf_debug('%s succeed in %s.'%(key,s_name))
                else: self.__logger.printf_debug('%s is empty.'%key)
            else:
                self.__logger.printf_debug("write new value is empty by {}.".format(key))

        else:
            self.end()
            raise ValueError("if you want to use write function,please set mode 'w'.")

    def append(self,key,value):
        if self.__mode == 'a':
            if key in self.__KEYS:
                s_name = self.__CHUNKED_INDEXS[key]
                fileIndex = self._get_file_index(s_name)

                # add primary_key
                if self.__primary_key != None and value.empty is False:
                    check = globals()[PARTITION_VARIABLE.format(fileIndex)]._built_in_read(key)
                    if check.empty is False:
                        if self.__primary_key not in check.columns and self.__primary_key not in value.columns:
                            self.end()
                            raise ValueError(
                                'if you want to check repeat values,please write current column but not "{}" and mode must be "hdfs".'.format(
                                    self.__primary_key))
                        else:
                            if len(set(check[self.__primary_key]) & set(value[self.__primary_key])) != 0:
                                # self.__logger.printf_debug("the new value is repeated by {}.".format(key))
                                raise ValueError("the new value is repeated by {} with primary key '{}'.".format(key,
                                                                                                                 self.__primary_key))
                            else:
                                globals()[PARTITION_VARIABLE.format(fileIndex)].append(key, value)
                    else:
                        globals()[PARTITION_VARIABLE.format(fileIndex)].append(key, value)

                else:
                    globals()[PARTITION_VARIABLE.format(fileIndex)].append(key, value)
            else:
                keyCounts = self._check_keys_count(mode='a')
                fileIndex = self._get_file_index(keyCounts[-1][0])
                globals()[PARTITION_VARIABLE.format(fileIndex)].write(key, value)
                globals()[FILE_KEYS_LIST.format(fileIndex)].append(key)
                self.__KEYS.append(key)
                s_name = STORE_NAME.format(self.__partition_name, fileIndex)
                self.__RE_CHUNKED_INDEXS[s_name] = globals()[FILE_KEYS_LIST.format(fileIndex)]

            if len(value) != 0:
                self.__logger.printf_debug('%s succeed in %s.' % (key, s_name))
            else:
                self.__logger.printf_debug('%s is empty.' % key)
        else:
            self.end()
            raise ValueError("if you want to use append function,please set mode 'a'.")


    def reload(self,key,value):
        if self.__mode == 'a':
            if key in self.__KEYS:
                s_name = self.__CHUNKED_INDEXS[key]
                fileIndex = self._get_file_index(s_name)
                if value.empty is False:
                    globals()[PARTITION_VARIABLE.format(fileIndex)].reload(key, value)
                else:
                    self.__logger.printf_debug("{}'s value is empty by reload.".format(key))

            else:
                self.__logger.printf_debug("{} not in keys by reload.".format(key))

            if len(value) != 0:
                self.__logger.printf_debug('%s succeed in %s.' % (key, s_name))
            else:
                self.__logger.printf_debug('%s is empty.' % key)
        else:
            self.end()
            raise ValueError("if you choose reload function,please set mode 'a'.")


    def update(self,key,value,column=None):
        if self.__mode == 'a':
            if key in self.__KEYS:
                s_name = self.__CHUNKED_INDEXS[key]
                fileIndex = self._get_file_index(s_name)
                check = globals()[PARTITION_VARIABLE.format(fileIndex)]._built_in_read(key)
                if check.empty is False and value.empty is False:
                        globals()[PARTITION_VARIABLE.format(fileIndex)].update(key, value, column)
                else:
                    self.__logger.printf_debug('check length %s,value length %s,not update' % (len(check), len(value)))
            else:
                self.__logger.printf_debug("{} not in keys by update".format(key))

            if len(value) != 0 : self.__logger.printf_debug('%s succeed in %s.'%(key,s_name))
            else: self.__logger.printf_debug('%s is empty.'%key)
        else:
            self.end()
            raise ValueError("the mode is '%s',you only can choose 'a'."%self.__mode)

    def add_column(self,key,column,default=None,is_null=True):
        if self.__mode == 'a':
            if key in self.__KEYS:
                s_name = self.__CHUNKED_INDEXS[key]
                fileIndex = self._get_file_index(s_name)
                check = globals()[PARTITION_VARIABLE.format(fileIndex)]._built_in_read(key)
                if check.empty is False :
                    globals()[PARTITION_VARIABLE.format(fileIndex)].add_column(key,column,default=default,is_null=is_null)
                    self.__logger.printf_debug('%s succeed in %s by add_columns.' % (key, s_name))
                else:
                    self.__logger.printf_debug('check length %s,not update by add_columns' % (len(check)))
            else:
                self.__logger.printf_debug("{} not in keys by add_columns".format(key))

        else:
            self.end()
            raise ValueError("the mode is '%s',you only can choose 'a'." % self.__mode)

    def del_column(self,key,column):
        if self.__mode == 'a':
            if key in self.__KEYS:
                s_name = self.__CHUNKED_INDEXS[key]
                fileIndex = self._get_file_index(s_name)
                check = globals()[PARTITION_VARIABLE.format(fileIndex)]._built_in_read(key)
                if check.empty is False :
                    globals()[PARTITION_VARIABLE.format(fileIndex)].del_column(key,column)
                    self.__logger.printf_debug('%s succeed in %s by del_columns.' % (key, s_name))
                else:
                    self.__logger.printf_debug('check length %s,not update by del_columns' % (len(check)))
            else:
                self.__logger.printf_debug("{} not in keys by del_columns".format(key))
        else:
            self.end()
            raise ValueError("the mode is '%s',you only can choose 'a'." % self.__mode)


    def remove(self,key):
        if key in self.__KEYS:
            s_name = self.__CHUNKED_INDEXS[key]
            fileIndex = self._get_file_index(s_name)
            globals()[FILE_KEYS_LIST.format(fileIndex)].remove(key)
            self.__KEYS.remove(key)
            del self.__CHUNKED_INDEXS[key]
            remove_reindex(self.__RE_CHUNKED_INDEXS,key)
        else:
            self.__logger.printf_debug("{} not in keys by remove".format(key))

    def end(self):
        if self.__mode == 'w':
            for chunk_i in  range(0,self.__chunk):
                globals()[PARTITION_VARIABLE.format(chunk_i)].end()
        elif self.__mode in ['a','r']:
            for s_name in self.__partitions:
                chunk_i = self._get_file_index(s_name)
                globals()[PARTITION_VARIABLE.format(chunk_i)].end()
        else:
            raise ValueError('please choose current mode.')

        self.__CHUNKED_INDEXS = {}
        for k,v in self.__RE_CHUNKED_INDEXS.items():
            for j in v:
                self.__CHUNKED_INDEXS[j] = k
        self.__partitions = list(self.__RE_CHUNKED_INDEXS.keys())
        sets = {
            'keys': self.__KEYS,
            'index': self.__CHUNKED_INDEXS,
            'reindex': self.__RE_CHUNKED_INDEXS,
            'partitions': self.__partitions,
            'position':self.__FILE_POSITIONS
        }
        joblib.dump(sets, self.__index_path+ INDEX_FILE.format(self.__partition_name))

    def read(self,key):
        if key in self.__KEYS:
            s_name = self.__CHUNKED_INDEXS[key]
            fileIndex = self._get_file_index(s_name)
            return globals()[PARTITION_VARIABLE.format(fileIndex)].read(key)
        else:
            self.__logger.printf_debug("{} not in keys by read".format(key))


    @property
    def keys(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['keys']

    @property
    def index(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['index']

    @property
    def reindex(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['reindex']

    @property
    def partitions(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['partitions']

    @property
    def positions(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['position']

    # 更新json中的路径信息
    def update_positions(self):
        json = joblib.load(self.__index_path + INDEX_FILE.format(self.__partition_name))
        json['position'] = get_FILE_POSITIONS(self.__sub_store,self.__partitions)
        return joblib.dump(json,self.__index_path + INDEX_FILE.format(self.__partition_name))








