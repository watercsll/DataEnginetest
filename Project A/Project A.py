import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
# 请求URL
def get_page_content(base_url):
# 得到页面的内容
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(base_url,headers=headers,timeout=10)
    content = html.text 
    # 通过html字符串创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')   
    return soup

#分析价格及图片
def analysis(soup):
    result_list = soup.find('div',class_='search-result-list')
    #提取车型及价格信息
    df = pd.DataFrame(columns =['car_model','lowest_price','highest_price','pic_link'])
    item_list = result_list.find_all('p')   
    #pirnt(item_list)
    
    #提取图片网址    
    pic_list = soup.find_all('img',class_ = 'img')
    #print(pic_list)
    
    #循环提取价格及网址
    for i in range(int(len(item_list)/3)):        
        temp = {}
        
        #获取并加工价格数据
        car_model = item_list[i*3].text
        #print(car_model)
        car_price = item_list[i*3+1].text
        if car_price != "暂无":           
            lowest_price = car_price[0:5]+"万"
            highest_price = car_price[6:]
        else:
            lowest_price = "暂无"
            highest_price = "暂无"
        #print(lowest_price)
        #print(highest_price)
            
        #获取并加工图片链接
        pic = str(pic_list[i])   
        pattern = '//img.*.??g'
        head = 'http:'
        pic_link = ''.join(re.findall(pattern,pic))
        pic_link = head + pic_link
        print(pic_link)
        
        #整合汇总
        temp['car_model'],temp['lowest_price'],temp['highest_price'],temp['pic_link'] = car_model,lowest_price,highest_price,pic_link
        df = df.append(temp,ignore_index = True)
        i = i+1  
    return df


base_url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
# 创建一个DataFrame
result = pd.DataFrame(columns =['car_model','lowest_price','highest_price','pic_link'])
soup = get_page_content(base_url)
df = analysis(soup)
result = result.append(df)
result.to_csv('VWBrandCar.csv')
