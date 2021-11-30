#!/usr/bin/env python
# coding: utf-8

# In[426]:


import requests
import bs4
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pandas import DataFrame


# In[503]:


#first step, download all comments of specific movie from metacritic website by using beautifulsoup
def comments_download(url,header):
    try:
        r = requests.get(url,headers=header)
        r.encoding = 'UTF-8'
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        #html_content = BeautifulSoup(r.text,'html.parser')
        html_content = BeautifulSoup(r.text,'lxml')
        return(html_content)
    except:
        print('download failed!')
    #parser downloaded html content
#url = 'https://www.metacritic.com/movie/shang-chi-and-the-legend-of-the-ten-rings?ftag=MCD-06-10aaa1c'
url = 'https://www.metacritic.com/movie/shang-chi-and-the-legend-of-the-ten-rings/user-reviews'
#url = 'https://www.metacritic.com/movie/shang-chi-and-the-legend-of-the-ten-rings/user-reviews?page=1'
#url = 'https://www.metacritic.com/movie/shang-chi-and-the-legend-of-the-ten-rings/user-reviews?page=2'
header_info = {'user-agent':'Mozilla/5.0'}
html_contents = comments_download(url,header_info)


# In[506]:


def single_page(html_contents):
    #get the comment of html_contents, object type is beautifulsoup
    results = []
    for tags in html_contents.find_all('div','review pad_top1'):
        for child in tags.descendants:
            if(child.name=='div'):
                if child.find('span','author') != None:
                    author = child.find('span','author').get_text()
                if child.find('span','date') != None:
                    date = child.find('span','date').get_text()
                if child.find('span','yes_count')!= None:
                    yes_count = child.find('span','yes_count').get_text()
                if child['class'][0] == 'metascore_w':
                    score = str(child.string)
            if(len(list(tags.find('div','review_body').descendants)))>4:
                if isinstance(child,bs4.Tag) and isinstance(child.find('span'),bs4.Tag) and len(child['class'])>1:
                    if child['class'][1]=='inline_collapsed':
                        comment = child.get_text().replace('…','').replace('Expand','')
                    else:
                        if child.find('div','review_body') != None:
                            comment = child.find('div','review_body').get_text().strip()
            else:
                if isinstance(child,bs4.Tag):
                    comment_tmp = child.find('div','review_body')
                    if comment_tmp != None:
                        comment = comment_tmp.get_text().strip()
        #single_result = author+'\t'+date+'\t'+yes_count+'\t'+score+'\t'+comment
        single_result = [author,date,yes_count,score,comment]
        results.append(single_result)
    result_df = pd.DataFrame(results)
    result_df.columns = ['user','date','upvote','score','comment']
    return(result_df)
#single_df = single_page(html_contents)


# In[507]:


def total_pages(page_num):
    i=0
    page_comment = []
    while i < page_num:
        url = 'https://www.metacritic.com/movie/shang-chi-and-the-legend-of-the-ten-rings/user-reviews?page='+str(i)
        i+=1
        #print(url)
        single_html_contents = comments_download(url,header_info)
        single_page_df = single_page(single_html_contents)
        page_comment.append(single_page_df)
    total_df = pd.concat(page_comment)
    return(total_df)
total_result_df = total_pages(3)


# In[508]:


total_result_df.to_csv('total_comment_shang_chi.csv',encoding='utf-8')


# In[509]:


total_result_df.info()


# In[510]:


total_result_df.head()


# In[463]:


import pandas_bokeh
pandas_bokeh.output_notebook()
pd.set_option('plotting.backend', 'pandas_bokeh')
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral
from bokeh.io import curdoc


# In[511]:


df_test = total_result_df


# In[512]:


df_test['time'] = pd.to_datetime(df_test.date).dt.date


# In[513]:


df_test.head()


# In[520]:


date_comment_num = df_test.groupby('time').nunique()#.to_frame('comment_num')
#print(date_comment_num)
#print(date_comment_num.shape)
date_comment_num.index = date_comment_num.index.astype('string')
y = date_comment_num['comment']
mapper = linear_cmap(field_name='comment', palette=Spectral[11] ,low=min(y) ,high=max(y))
date_bar = date_comment_num.plot_bokeh.bar(
    ylabel="comment number", 
    title="comment number by date", 
    color=mapper,
    alpha=0.8,
    legend=False    
)


# In[524]:


df_test['comment_len'] = df_test['comment'].str.len()
df_test['comment_len'] = df_test['comment_len'].fillna(0).astype(int)
contentlen_hist = df_test.plot_bokeh.hist(
    y='comment_len',
    ylabel="comment_num", 
    bins=np.linspace(0, 100, 26),
    vertical_xlabel=True,
    hovertool=False,
    title="comment len bar",
    color='red',
    line_color="white",
    legend=False,
#     normed=100,
    )


# In[525]:


from wordcloud import WordCloud


# In[526]:


df_test.head()


# In[532]:


all_comments = ' '.join(df_test['comment'].to_list())


# In[533]:


wc = WordCloud()
wc.generate(all_comments)


# In[534]:


import matplotlib.pyplot as plt
plt.imshow(wc)
plt.axis("off")


# In[ ]:





# In[423]:


type(html_contents)


# In[314]:


num=0
for tags in html_contents.find_all('div',{'class':'review pad_top1'}):
    #print(tags)
    num+=1
    if num ==5:
        #print(tags)
        print('test')
        #print(tags.find('div','review_body').contents)
        #for child in tags.find('div','review_body').descendants:
            #comment = ' '.join(child.find_all(text=True))
            #print(comment)
        #    print(child)
        #    print(child.name)
        print(len(list(tags.find('div','review_body').descendants)))
    if num == 6:
        print('short comment.....')
        print(len(list(tags.find('div','review_body').descendants)))
        #for child in tags.find('div','review_body').descendants:
            #print(child)
            #if child.name =='span' and len(child['class']):
            #print(type(child))
            #print(child.name)
            #if child.find('span')!=None:
                
        #print(tags.find('div','review_body').contents)


# In[215]:


for child in html_contents.find_all('div','review pad_top1'):
    for tmp in child.descendants:
        print(tmp)

