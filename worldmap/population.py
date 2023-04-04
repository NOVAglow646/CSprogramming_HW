from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Map
import pandas as pd
import json

data = pd.read_excel('./data/1960-2021年全球各国人数量.xlsx', usecols=[0,64])
# 2020年全国人口数据
ide=data.index.values

dict={data['国家'][i]:data[2021][i] for i in range(len(ide))}
#print(dict)

with open("./country.json",'r') as f:
    name_map = json.load(f)

 
en_dict={}

for en,ch in name_map.items():
    if ch in dict.keys():
        en_dict[en]=int(dict[ch])

map_data = list(en_dict.items())
print(map_data)
c = (
    Map()
    .add("2021年世界人口", 
         data_pair=map_data, 
         maptype="world",
         is_map_symbol_show=False, # 不描点             
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False)) #不显示标签
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2021年世界人口"),
        visualmap_opts=opts.VisualMapOpts(min_=60, max_=150000000),
    )
)

c.render('./output/世界人口.html')