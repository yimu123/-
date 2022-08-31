import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data = pd.read_csv('./Data_bouban_2.csv',encoding='utf-8')
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