import pandasfiles as pf
import numpy as np
import pandas as pd
import joblib
from pandasfiles.base.craft import Craft






#
if __name__ == '__main__':
    import tushare as ts
    dis = pf.Distribution(chunk=2,mode='a',auto=True,primary_key='date')
    # dis.start()
    # stock_data = ['600115','000400']
    # for i in stock_data:
    #     name = 'st'+i
    #     zz = ts.get_k_data(i,start='2018-01-01',end='2018-10-03')
    #     dis.write(name,zz)
    # dis.end()
    print(dis.read('st600115'))
    dis.start()
    dis.add_column('st600115',column='zz')
    dis.end()
    # dis.start()
    # a = pd.DataFrame({'high':[1,2,3],'low':[2345,234,1],'date':['2018-01-03','2018-01-02','2018-01-05']})
    # print(a)
    # dis.update('st600115',a,column='date')
    # dis.end()
    print(dis.read('st600115'))
