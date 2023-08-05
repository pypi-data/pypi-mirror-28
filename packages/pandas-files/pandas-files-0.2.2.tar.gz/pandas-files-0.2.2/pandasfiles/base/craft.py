# coding:utf-8
import pandas as pd
import numpy as np
import joblib
from pandasfiles.utils.tools import find_path


class Craft:

    def __init__(self,mode,store_path='',store_name=''):
        self.mode = mode
        if '.h5' in str(store_name):
            self.s_name = store_name
        else:
            raise ValueError('store_name must named xxx.h5,please check it.')

        if store_path == '':
            self.s_path = find_path('tmp')
        else:
            self.s_path = store_path

    def start(self):
        if self.mode == 'w':
            self.hdfs = pd.HDFStore(self.s_path + self.s_name, mode='w', complevel=9, complib='blosc')
        elif self.mode == 'a':
            self.hdfs = pd.HDFStore(self.s_path + self.s_name, mode='a', complevel=9, complib='blosc')
        elif self.mode == 'r':
            self.hdfs = pd.HDFStore(self.s_path + self.s_name, mode='r', complevel=9, complib='blosc')
        else:
            raise ValueError('the mode can be selected "w","a" and "r".')

    def read(self,key):
        resp = self.hdfs[key]
        return resp


    def _built_in_read(self,key):
        resp = self.hdfs[key]
        return resp


    def write(self,key,value):
        if self.mode in ['w','a']:
            if '/'+key in self.hdfs.keys():
                self.append(key,value,reset_index=False)
            else:
                self.hdfs[key] = value
            return self.hdfs[key]
        elif self.mode == 'r':
            raise ValueError("the mode is 'r',you only can read.")

    def reload(self,key,value):
        if self.mode in ['w','a']:
            self.hdfs[key] = value
            return self.hdfs[key]
        elif self.mode == 'r':
            raise ValueError("the mode is 'r',you only can read.")

    def remove(self,key):
        del self.hdfs[key]
        return True

    def append(self,key,value,reset_index=True):
        if self.mode in ['w','a']:
            self.hdfs[key] = self.hdfs[key].append(value)
            if reset_index == True : self.hdfs[key] = self.hdfs[key].reset_index(drop=True)
            return self.hdfs[key]
        elif self.mode == 'r':
            raise ValueError("the mode is 'r',you only can read.")

    def update(self,key,value,column=None):
        if self.mode in ['w','a']:
            if column == None:
                tmp = self.hdfs[key]
                tmp.update(value)
                self.hdfs[key] = tmp.reset_index(drop=True)
                del tmp
            else:
                tmp = self.hdfs[key]
                tmp.index = tmp[column]
                value.index = value[column]
                tmp.update(value)
                self.hdfs[key] = tmp.reset_index(drop=True)
                del tmp
            return self.hdfs[key]
        elif self.mode  == 'r':
            raise ValueError("the mode is 'r',you only can read.")

    def add_column(self,key,column,default=None,is_null=True):
        if self.mode in ['w','a']:
            if is_null == True:
                tmp = self.hdfs[key]
                tmp[column] = np.NaN
                self.hdfs[key] = tmp
                del tmp
            else:
                if default != None:
                    tmp = self.hdfs[key]
                    tmp[column] = default
                    self.hdfs[key] = tmp
                    del tmp
                raise ValueError('if you set not null,please give a value to default.')
            return self.hdfs[key]
        elif self.mode == 'r':
            raise ValueError("the mode is 'r',you only can read.")

    def del_column(self,key,column):
        if self.mode in ['w','a']:
            tmp = self.hdfs[key]
            if column in tmp.columns:
                del tmp[column]
                self.hdfs[key] = tmp
                del tmp
                return self.hdfs[key]
            else:
                return None
        elif self.mode  == 'r':
            raise ValueError("the mode is 'r',you only can read.")

    def end(self):
        self.hdfs.close()



