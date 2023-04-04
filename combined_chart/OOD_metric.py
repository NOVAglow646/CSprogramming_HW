from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line
import numpy as np
from scipy.stats import pearsonr

epochs=[i for i in range(0,100,10)]
test_acc=[ round(x,2) for x in np.random.uniform(low=0.6, high=0.7, size=(10))]
val_acc=[round(x+float(np.random.uniform(low=-0.05, high=0.05)),2) for x in test_acc]
EI=[round(x*0.5 * float(np.random.uniform(low=0.8, high=1.2)),2) for x in test_acc]
pearson1=[round(pearsonr(val_acc,test_acc)[0],3) for _ in range(10)]
pearson2=[round(pearsonr(EI,test_acc)[0],3) for _ in range(10)]

bar = (
    Bar()
    .add_xaxis(epochs)
    .add_yaxis(
        "测试集准确率",
        test_acc,
        yaxis_index=0,
        color="#d14a61",
    )
    .add_yaxis(
        "验证集准确率",
        val_acc,
        yaxis_index=1,
        color="#5793f3",
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="测试集准确率",
            type_="value",
            min_=0,
            max_=1,
            position="right",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#d14a61")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} "),
        )
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="相关系数",
            min_=0,
            max_=1,
            position="left",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#675bba")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} "),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            name="验证集准确率",
            min_=0,
            max_=1,
            position="right",
            offset=80,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#5793f3")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} "),
        ),
        title_opts=opts.TitleOpts(title="机器学习中分布外测试准确率\n和分布内指标的关系"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(pos_left="25%"),
    )
)

line = (
    Line()
    .add_xaxis(epochs)
    .add_yaxis(
        "相关系数",
        pearson1,
        yaxis_index=2,
        color="#675bba",
        label_opts=opts.LabelOpts(is_show=False),
    )
)

bar1 = (
    Bar()
    .add_xaxis(epochs)
    .add_yaxis(
        "测试集准确率",
        test_acc,
        color="#d04a51",
        xaxis_index=1,
        # y轴索引，继上面的 设为3
        yaxis_index=3,
    )
    .add_yaxis(
        "Efficient score",
        EI,
        color="#5793f3",
        xaxis_index=1,
        yaxis_index=3,
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="测试集准确率",
            type_="value",
            min_=0,
            max_=1,
            position="right",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#d14a61")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} "),
        )
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="相关系数",
            min_=0,
            max_=1,
            position="left",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#675bba")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(grid_index=1),
        yaxis_opts=opts.AxisOpts(
            name="验证集准确率",
            min_=0,
            max_=1,
            position="right",
            offset=80,
            # 直角坐标系网格索引
            grid_index=1,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#5793f3")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} "),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(pos_left="65%"),
    )
)

line1 = (
    Line()
    .add_xaxis(epochs)
    .add_yaxis(
        "相关系数",
        pearson2,
        color="#675bba",
        label_opts=opts.LabelOpts(is_show=False),
        # 新增了一个 x轴的索引，上面的line中x轴的索引为0
        xaxis_index=1,
         
        yaxis_index=5,
    )
)

overlap_1 = bar.overlap(line)
overlap_2 = bar1.overlap(line1)


# 使用grid将overlap_1和overlap_2进行水平并行放置
grid = (
        # 初始化
    Grid(init_opts=opts.InitOpts(width="1200px", height="800px"))
    .add(
        overlap_1, grid_opts=opts.GridOpts(pos_right="58%"), 
        # 是否由自己控制 Axis 索引
        is_control_axis_index=True
    )
    .add(overlap_2, grid_opts=opts.GridOpts(pos_left="58%"), is_control_axis_index=True)
    .render("./output/OOD_metrics.html")
)
