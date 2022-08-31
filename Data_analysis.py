import pandas as pd
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.misc import imread
import pygal.maps.world
import numpy as np
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType




#读取数据文件
data = pd.read_csv('./Data_bouban_2.csv',encoding='utf-8')
with open('label.txt', 'a') as fp:
    for i in data['标签']:
        fp.write(str(i))
        fp.write(',')
'''
生成词云图
'''
#文件名
word_file= 'label.txt'
#读取文件内容
word_content=open(word_file,'r',encoding='gbk').read().replace('\n','')
#设置背景图片
img_file='./heart.jpg'
#读取背景图片
mask_img=imread(img_file)
#进行分词
word_cut=jieba.cut(word_content)
#把分词用空格连起来
word_cut_join=" ".join(word_cut)
#生成词云
wc=WordCloud(
            font_path='simfang.ttf',#设置字体
            max_words=28,#词云显示的最大词数
            mask=mask_img,#设置背景图片
            background_color='white',#背景颜色
            collocations=False
            ).generate(word_cut_join)

plt.imshow(wc)
#去掉坐标轴
plt.axis('off')
#将图片保存到本地
plt.savefig('词云.jpg')
plt.show()


'''
国家分布饼图
'''
word_content = list(data['国家'])
#将data['国家']中的数据按，分割转化成列表
content = []
for i in word_content:
    s =str(i).split(',')
    content.extend(s)
#去除列表中每个元素里面的空格
for i in range(len(content)):
    content[i] = content[i].replace(' ','')
#统计列表中每个国家出现的次数并存在字典中
dict = {}
for key in content:
    dict[key] = dict.get(key, 0) + 1
# print(dict)
#存放标签
label = []
#存放数据
num = []
count = 0
for i in dict:
    if dict[i] > 1000:
        label.append(i)
        num.append(dict[i])
    else:
        count += dict[i]
label.append('其他')
num.append(count)
#自定义颜色
colors = ['red', 'pink', 'magenta', 'purple', 'orange','green','blue','grey']
plt.axes(aspect='equal')
plt.xlim(0,8)
plt.ylim(0,8)
plt.gca().spines['right'].set_color('none')

plt.gca().spines['top'].set_color('none')

plt.gca().spines['left'].set_color('none')

plt.gca().spines['bottom'].set_color('none')
plt.pie(x=num, #绘制数据
    labels=label,#添加编程语言标签
    colors=colors, #设置自定义填充色
    autopct='%.3f%%',#设置百分比的格式,保留3位小数
    pctdistance=0.8, #设置百分比标签和圆心的距离
    labeldistance=1.0,#设置标签和圆心的距离
    startangle=180,#设置饼图的初始角度
    center=(4,4),#设置饼图的圆心(相当于X轴和Y轴的范围)
    radius=3.8,#设置饼图的半径(相当于X轴和Y轴的范围)
    counterclock= False,#是否为逆时针方向,False表示顺时针方向
    wedgeprops= {'linewidth':1,'edgecolor':'green'},#设置饼图内外边界的属性值
    textprops= {'fontsize':12,'color':'black'},#设置文本标签的属性值
    frame=1) #是否显示饼图的圆圈,1为显示
#去除xy轴的坐标值
plt.xticks(())
plt.yticks(())
#添加图形标题
plt.title('豆瓣电影分布图')
#防止中文出现乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
#保存图片
plt.savefig('国家分布—饼图.jpg')
#显示图形
plt.show()


'''
国家分布世界地图
'''
worldmap_chart = pygal.maps.world.World()
worldmap_chart.title = '豆瓣电影世界分布图'
worldmap_chart.add('In 2021', {
  'us': 7762,
  'cn': 3201,
  'hk': 1974,
  'fr': 1869,
  'jp': 2012,
  'gb': 2203,
  'kr': 1010,
  'de': 998,
  'it': 522,
  'au': 293,
  'es': 376,
  'id': 192,
  'be': 263,
  'ru': 186,
  'nl': 126,
  'pl': 122,
  'th': 191,
  'se': 158,
  'dk': 145,
  'ch':109,
  'ie':130
})
worldmap_chart.render_to_file('bar_chart.svg')

'''
电影评分区间数量统计
'''
area = data['评分']
x1 = ['<5','5-6','6-7','7-8','8-9','>9']
y1 = np.zeros(6)
for i in range(len(area)):
    if area[i]<=5:
        y1[0]+= 1
        continue
    if area[i]<=6:
        y1[1]+= 1
        continue
    if area[i]<=7:
        y1[2]+= 1
        continue
    if area[i]<=8:
        y1[3]+= 1
        continue
    if area[i]<=9:
        y1[4]+= 1
        continue
    if area[i]>9:
        y1[5]+= 1
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(x1)
    .add_yaxis("数量", y1.tolist())
    .set_global_opts(title_opts=opts.TitleOpts(title="电影评分/数量统计"),
                    yaxis_opts=opts.AxisOpts(name="数量"),
                     xaxis_opts=opts.AxisOpts(name="评分区间"))
)
bar.render_notebook()


'''
高分电影国家分布=柱状图
'''
country = []
num = 0
for i in range(len(data['评分'])):
    if data['评分'][i] >= 9.0:
        num += 1
        country.append(data['国家'][i])
#将data['国家']中的数据按，分割转化成列表
content = []
for i in country:
    s =str(i).split(',')
    content.extend(s)
#去除列表中每个元素里面的空格
for i in range(len(content)):
    content[i] = content[i].replace(' ','')
#统计列表中每个国家出现的次数并存在字典中
dict = {}
for key in content:
    dict[key] = dict.get(key, 0) + 1
label = []
number = []
count = 0
for key in dict:
    if dict[key] >= 20:
        label.append(key)
        number.append(dict[key])
    else:
        count += dict[key]
label.append('其他')
number.append(count)
plt.bar(range(len(number)), number, color=['r', 'g', 'b', 'c', 'm', 'y'], tick_label=label)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.title('高分电影分布情况')
index=np.arange(len(label))
#柱子上的数字显示
for a,b in zip(index,number):
    plt.text(a,b+0.05,"%.0f" %b, ha='center',va='bottom',fontsize=11)
plt.savefig('高分电影分布-柱状图.jpg')
plt.show()