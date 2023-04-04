import pandas as pd                         #读取excel
from pyecharts import options as opts       #可视化选项
from pyecharts.charts import Timeline,Map   #时间线、地图
from pyecharts.globals import ThemeType,CurrentConfig,NotebookType     #图表主题

#数据源https://github.com/BlankerL/Covid-COVID-19-Data
Covid_file = './data/DXYArea.csv'
list_color = ['#color','#color','#color','#color','#color']
Covid = pd.read_csv(Covid_file, usecols =         ['countryEnglishName','provinceName','province_confirmedCount','updateTime'])
Covid0 = Covid[(Covid.countryEnglishName == 'China')]
Covid1 = Covid0[['provinceName','province_confirmedCount','updateTime']]

#类型转换
Covid1['updateTime'] = Covid1['updateTime'].astype(str).str[0:10]
#按省份分组统计
Covid11 = Covid1.groupby(['provinceName','updateTime']).apply(lambda t:         t[t.province_confirmedCount == t.province_confirmedCount.max()])
Covid11 = Covid11[['provinceName','province_confirmedCount','updateTime']]
Covid11 = Covid11.drop_duplicates()         #删除重复值
Covid2 = Covid11.reset_index(drop=True)     #重置索引
Covid2.head()
print(Covid2)


covid_list= [Covid2[Covid2['updateTime'].str.contains("2022-12-{}".format(i))] for i in range(0,15)]
print(covid_list)

def ltimeline() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(page_title="疫情地图",
                    theme=ThemeType.CHALK,
                    width="1000px",     #图像宽度
                    height="800px"),
    )
    for idx in range(10, 15):
        provinces = []
        confirm_value = []
        for item_pv in covid_list[idx]['provinceName']:
            provinces.append(item_pv)
        for item_pc in covid_list[idx]['province_confirmedCount']:
            confirm_value.append(item_pc)
        zipped = zip(provinces,confirm_value)   #组合两个字段
        f_map = (
            Map(init_opts=opts.InitOpts(width="800px",
                                        height="500px",
                                        page_title="疫情地图",
                                        bg_color=None))
            .add(series_name="确诊数量",
                    data_pair=[list(z) for z in zipped],
                    maptype="china",
                    is_map_symbol_show=False)
            .set_global_opts(
                #设置标题
                title_opts=opts.TitleOpts(title="2022年12月全国疫情地图",
                                        subtitle="12月{}日-当天数据\n"
                                        "......".format(idx + 1),
                                        pos_left="center",),
                #设置图例
                legend_opts=opts.LegendOpts(
                    is_show=True, pos_top="40px", pos_right="30px"),
                #设置视觉映射
                visualmap_opts=opts.VisualMapOpts(
                    is_piecewise=True, range_text=['高','低'], pieces=[   #分段显示
                        {"min": 10000, "color": "#642100"},
                        {"min": 1000, "max": 9999,"color": "#a23400"},
                        {"min": 500, "max": 999, "color": "#bb5e00"},
                        {"min": 100, "max": 499, "color": "#ff8000"},
                        {"min": 10, "max": 99, "color": "#ffaf60"},
                        {"min": 1, "max": 9, "color": "#ffd1a4"},
                        {"min": 0, "max": 0, "color": "#fffaf4"}
                    ]),
            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True),
                             markpoint_opts=opts.MarkPointOpts(
                                 symbol_size=[90,90],symbol='circle'),
                             effect_opts=opts.EffectOpts(is_show='True',)
                             )
        )
        tl.add(f_map, "{}日".format(idx + 1))
        tl.add_schema(is_timeline_show=True,    #是否显示
                    play_interval=1000,         #播放间隔
                    symbol=None,                #图标
                    is_loop_play=True           #循环播放
                    )
    return tl

ltimeline().render("./output/covid.html")
