# coding:utf-8
import os
from pandasfiles.base.distributed import Distribution
from pandasfiles.utils.tools import get_config


def checkBoolean(string):
    if string == 'True':
        return True
    elif string == 'False':
        return False
    else:
        raise ValueError('error')



class Setting(Distribution):


    def __init__(self,mode='w',chunk=1,conf_path='',auto=False,primary_key=None):
        if mode in ['w','a','r','r+']:
            self.mode = mode
        else:
            raise ValueError("mode only can be 'w' , 'a' , 'r' , 'r+'.")


        if auto == True:
            self.index_path = os.path.dirname(os.path.dirname(__file__)) + '/tmp'
            self.temp_path = os.path.dirname(os.path.dirname(__file__)) + '/tmp'
            self.partition_name = 'fgit'
            self.chunk = chunk
            self.log_file_path = ''
            self.silent = False
            sub_sections = {i: self.temp_path for i in range(0,chunk)}

        else:
            sections = get_config(conf_path)
            if 'main' not in sections.keys():
                raise ValueError('please set craft config,try again.')
            else:
                if 'index_path' in sections['main'].keys():
                    self.index_path = sections['main']['index_path']
                else:
                    self.index_path = os.path.dirname(os.path.dirname(__file__)) + '/tmp'

                if 'partition_name' in sections['main'].keys():
                    self.partition_name = sections['main']['partition_name']
                else:
                    self.partition_name = 'fgit'

                if 'chunk' in sections['main'].keys():
                    self.chunk = int(sections['main']['chunk'])
                else:
                    self.chunk = chunk

                if 'log_file_path' in  sections['main'].keys():
                    self.log_file_path = sections['main']['log_file_path']
                else:
                    self.log_file_path = ''

                if 'silent' in sections['main'].keys():
                    self.silent =  checkBoolean(sections['main']['silent'])
                else:
                    self.silent = False

                if 'temp_path' in sections['main'].keys():
                    self.temp_path = sections['main']['temp_path']
                    sub_sections = {i: self.temp_path for i in range(0, chunk)}
                else:
                    sub = [ i for i in sections.keys() if i !='main']
                    if len(sub) != self.chunk:
                        raise ValueError('please Make others settings counts equals to chunk size (%s != %s).'%(len(sub),self.chunk))
                    else:
                        # 结点的索引和存储方式
                        sub_sections = {int(sections[i]['index']):sections[i]['temp_path']  for i in sub}


        Distribution.__init__(self,
                              partition_name=self.partition_name,
                              chunk=self.chunk,
                              mode=self.mode,
                              index_path=self.index_path,
                              sub_store=sub_sections,
                              log_file_path=self.log_file_path,
                              silent=self.silent,
                              primary_key=primary_key)


