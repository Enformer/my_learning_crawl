#!/usr/bin/env python
#coding=utf-8

# 爬取三国演义
import requests
from lxml import etree
import os
from time import sleep
import re

# 设置请求头参数
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}

# 得到主页面的源码
def get_text_html(url):
    try:
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding
        html = response.text
        return html
    except:
        print("请求失败")

# 解析主页面，找到对应的章节页面url
def analyze_html(html):
    urls = []
    tree = etree.HTML(html)
    li_list = tree.xpath('//*[@id="main_left"]/div/div[4]/ul/li')
    for li in li_list:
        detail_url = 'https://www.shicimingju.com' + li.xpath('./a/@href')[0]
        urls.append(detail_url)
    return urls

# 分析章节页面源码找到具体文本内容地址，并实现持久化存储
def analyze_detail(d_urls):
    for d_url in d_urls:
        d_html = get_text_html(d_url)
        d_tree = etree.HTML(d_html)
        d_p_list = d_tree.xpath('//*[@id="main_left"]/div[1]/div/p')
        global title # 使title成为全局变量，可以被download_txt()函数调用
        title = d_tree.xpath('//*[@id="main_left"]/div[1]/h1/text()')[0]
        for d_p in d_p_list:
            details = d_p.xpath('./text()')[0]
            content = re.sub('&nbsp;', '', details)  # 删除&nbsp;
            download_txt(content)
            sleep(1) # 下完一段，延迟1秒
        print(title, "下载成功")

# 下载三国演义每个章节，并存储在对应章节标题的txt文件中
def download_txt(txt):
    if not os.path.exists('三国演义'):
        os.mkdir('三国演义')
    with open('./三国演义' + '/' + title + '.txt', 'a', encoding='utf-8') as f:
        f.write(txt)
    f.close()

# 执行主函数
def main():
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html' # 给定主页面url
    html = get_text_html(url)
    d_urls = analyze_html(html)
    analyze_detail(d_urls)


main()
