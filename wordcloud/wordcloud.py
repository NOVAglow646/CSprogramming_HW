# -*- coding: utf-8 -*-
from pyecharts.charts import WordCloud

##-------从文件中读出人物词频------------------
src_filename = './output/球状闪电-非人物地点名词词频-pseg.csv'
# 格式：人物,出现次数

src_file = open(src_filename, 'r')
line_list = src_file.readlines()  #返回列表，文件中的一行是一个元素
src_file.close()

print(line_list)  # 检查读入数据的情况

# 将读入的每行数据拆分成元组
wordfreq_list = []  #用于保存元组(人物姓名,出现次数)
for line in line_list:
    line = line.strip()  #删除'\n'
    line_split = line.split(',') # 以逗号作为标志，把字符串切分成词，存在列表中
    wordfreq_list.append((line_split[0],line_split[1]))

print(wordfreq_list)

del wordfreq_list[0] #删除csv文件中的标题行
##-------从文件中读出人物词频完成------------------

##===============================================
##-------生成词云---------------------------------
cloud = WordCloud() # 初始化词云对象

# 向词云中添加内容，第一个参数可以设为空，第二个参数为元组列表（词和词频）
cloud.add('', wordfreq_list)

# render会生成HTML文件。默认是当前目录render.html，也可以指定文件名参数
out_filename = './output/wordcloud_rd_file.html'
cloud.render(out_filename)

print('生成结果文件：' + out_filename)

