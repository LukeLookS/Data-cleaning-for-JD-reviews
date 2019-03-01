# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 16:07:12 2019

@author: Mengjie Shi

version 1.0
    去除单一重复字符
version 1.5
    去除html格式残留 eg. &gt 以及\n\t\r
    去除评论中出现次数大于4的数字
    去除开头末尾不必要的中英文特殊字符
version 2.0
    通过计算信息有效度，去除无效信息
"""

import pandas as pd
import numpy as np
# 需要pip install zhon
from zhon.hanzi import punctuation as chp
import string
import re

data=pd.read_csv('binary_test.csv',header=None)
data.head(5)
data.columns=['evaluation','name','content']

#用于提取中文的正则表达式
condition_chinese=u'[^\u4e00-\u9fa5]'
#用于提取英文的正则表达式
condition_english=u'[^a-zA-Z]'
fil_chinese = re.compile(condition_chinese, re.UNICODE)   
fil_english = re.compile(condition_english, re.UNICODE)   
# 记录用有的行号
recode=[]
for i in range(0,len(data)):
#    重置条件
    condition2=10
#    取出内容
    sample=data.loc[i,'content']
    ss=list(set(sample))
    ss=''.join(ss)
#    计算信息有效度
    condition1=len(ss)/len(sample)
#    取出中文内容
    txt_chinese=fil_chinese.sub('', sample)  #把提取出来的直接删除。
#    取出英文内容
    txt_english=fil_english.sub('', sample)  #把提取出来的直接删除。
    
#    如果中文不是空，则计算中英文比例
    if not (txt_chinese==''):
        condition2=len(txt_english)/len(txt_chinese)
#    信息有效度在三分之一以上且中英文比例中文更多
    if not (condition1<0.33 or condition2>1):
        recode.append(i)

data=data.drop(columns='name')   
#取出有用的数据
data_clean=data.iloc[recode,:]

de_num=[]
row= data_clean.shape[0]
col= data_clean.shape[1]

# 去除html格式残留
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}
    
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr

def deletenum(strs):
    for i in range(0,10):
        if (int(strs.count(str(i))) > 4): # 去除内容中出现次数大于4的数字，如11111@很好
            strs = strs.replace(str(i),'')
    return strs

for i in range (0,row):
    strs = data_clean.iloc[i,1]
    #去除\n\t\r
    strs = "".join(strs.split())
    #去除html格式残留
    strs = replaceCharEntity(strs)
    #去除前后中英文字符
    strs = strs.strip(string.punctuation+chp)
    #去除多余数字
    strs = deletenum(strs)
    strs = strs.strip(string.punctuation+chp)
    #合成数据
    data_clean.iloc[i,1] = strs
    i+=1


#存放数据
data_clean.to_csv('clean_test_data.csv', encoding = "utf-8")
