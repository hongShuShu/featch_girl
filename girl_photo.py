# !/usr/bin/evn python3
# coding:utf-8
#
# 博客地址 http://cuiqingcai.com/3179.html

import requests
import os
from bs4 import BeautifulSoup


def featch_url(url):
    UserAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'User-Agent': UserAgent}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print('再试一次')
        return
    # concent是二进制的数据，一般下载图片、视频、音频、等多媒体内容用concent, 打印网页内容用text
    soup = BeautifulSoup(response.text,'html.parser')
    # li_list = soup.find_all('div', class_='all').find('a')
    # 查找all下div里所有a标签
    print(response.text)
    print(soup.find('div',class_='all'))
    a_list = soup.find('div',class_='all').find_all('a')
    for a in a_list:
        title = a.get_text()
        href = a['href']

        # 创建文件夹
        target_path = str(title).strip() # 压缩空格
        local_path = '/Users/hongShuShu/Desktop/photo'
        final_path = os.path.join(local_path,target_path)
        os.mkdir(final_path)
        os.chdir(final_path) # 切换文件夹

        html = requests.get(href,headers)
        if html.status_code != 200:
            break
        html_soup = BeautifulSoup(html.text,'html.parser')
        # 查找所有的span标签,获取第十个span标签中的文本也就是最后一个页面
        max_span = html_soup.find('div',class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1,int(max_span)+1):
            # 每组图的url地址
            page_url = href + '/' + str(page)
            # print(page_url)
            img_html = requests.get(page_url,headers=headers)
            if img_html.status_code != 200:
                break
            img_soup = BeautifulSoup(img_html.text,'html.parser')
            img_url = img_soup.find('div',class_='main-image').find('img')['src']
            # 妹子照片地址
            # print(img_url)
            # 取url倒数第四到第九位做为图片名字
            file_name = img_url[-9:-4]
            img = requests.get(img_url,headers=headers,stream=True)
            f = open(file_name+'.jpg','ab')
            f.write(img.content)
            f.close()

if __name__ == '__main__':
    url = 'http://www.mzitu.com/all'
    featch_url(url)

