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
    #     zz = ts.get_k_data(i,start='2018-01-01',end='2018-01-05').astype('str')
    #     dis.write(name,zz)
    # dis.end()
    dis.start()
    a = dis.read('st600115')
    print(a)
    dis.end()
    # def pdMerge(old, new,columns_type=None,to_merge='date'):
    #     trade_dates = set(new[to_merge].tolist()) | set(old[to_merge].tolist())
    #     merge = pd.DataFrame(columns=old.columns, index=trade_dates)
    #     merge = merge.sort_index()
    #     merge['date'] = merge.index
    #     old.index = old['date']
    #     merge.update(old)
    #     new.index = new['date']
    #     merge.update(new)
    #     if columns_type != None:
    #         for columns,c_type in columns_type.items(): merge[columns] = merge[columns].astype(c_type)
    #     return merge.reset_index(drop=True)
    # dis.start()
    # new = ts.get_k_data('600115',start='2018-01-05',end='2018-01-10').astype('str')
    # print(new)
    # df = pdMerge(a,new,columns_type={'date':'str',
    #                                  'open':'float',
    #                                  'close':'float',
    #                                  'high':'float',
    #                                  'low':'float',
    #                                  'volume':'float'})
    # print(df)
    # dis.reload('st600115',df)
    # dis.end()



