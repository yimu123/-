import pandas as pd

#读取数据文件
data = pd.read_csv('./Data_douban_1.csv',encoding='gbk')
#根据影片名称给文件去重
data = data.drop_duplicates(['影片名称'])
#去除掉国家、演员、标签中的引号和中括号
data['国家'] = data['国家'].str.replace("'","")
data['国家'] = data['国家'].str.replace("[","").str.replace("]","")
data['标签'] = data['标签'].str.replace("'","")
data['标签'] = data['标签'].str.replace("[","").str.replace("]","")
data['演员'] = data['演员'].str.replace("'","")
data['演员'] = data['演员'].str.replace("[","").str.replace("]","")
#将发布日期中的月/日去掉
data['发布日期'] = data['发布日期'].map(lambda i :i.split('/')[0])
# print(data['发布日期'])

#将预处理好的文件保存
data.to_csv('.\\Data_bouban_2.csv', sep=',', header=True, index=False)