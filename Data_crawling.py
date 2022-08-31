import csv,requests
import time
import re

#爬取标签及类型号
def Lables_crawling():
    # 定义请求的url
    url = 'https://movie.douban.com/chart'
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
    }
    # 发送请求
    res = requests.get(url=url, headers=headers)
    # 判断请求状态
    if res.status_code == 200:
        req = res.text
        ex = 'type_name=(.*?)&type=(.*?)&interval_id=100:90'
        labels = re.findall(ex,req)
    return labels
#发送请求获取电影数据
def Getdata(label,num):
    #定义url
    url = 'https://movie.douban.com/j/chart/top_list'
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
    }
    params = [] #用来存放请求的参数
    response = []   #用来存放获取的数据
    for i in range(10,0,-1):
        #定义请求的参数
        param={
            'type': label[1],
            'interval_id': f'{i*10}:{(i-1)*10}',
            'action':'',
            'start': num,
            'limit': '20',
        }
        params.append(param)
        for i in params:
            res = requests.get(url=url,headers=headers,params=i)
            if res.status_code == 200:
                response.append(res.json())     #将请求得到的数据已json格式存放在response中
    return response
#解析获取的数据
def ParseData(datas):
    results =[]     #存放解析后的数据
    for data in datas:
        if data:
            for i in data:
                if i:
                    for j in range(len(i)):
                        result = {
                            '影片名称':i[j].get('title'),
                            '评分':i[j].get('score'),
                            '发布日期':i[j].get('release_date'),
                            '国家':i[j].get('regions'),
                            '标签':i[j].get('types'),
                            '演员':i[j].get('actors'),
                            '投票人数':i[j].get('vote_count')
                        }
                        results.append(result)
    return results

#将数据写入CSV文件
def Writedata(results):
    headers = ['影片名称', '评分', '发布日期', '国家','标签','演员','投票人数']
    with open('Data_douban.csv', 'w', newline='',encoding='utf-8') as f:
        # 标头在这里传入，作为第一行数据
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

#定义主函数，把请求的页数作为传递参数
def main(nums):
    labels = Lables_crawling()
    datas = []  #存放爬到的数据
    for label in labels:
        for num in range(0,20*nums,20):
            data = Getdata(label,num)
            datas.append(data)
            time.sleep(3)
    if datas:
        results = ParseData(datas)
        if results:
            Writedata(results)

if __name__ == '__main__':
    main(10)