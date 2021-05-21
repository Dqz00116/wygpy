# -*- coding: utf-8 -*-
"""
    作者：源渋 d_qz@foxmai.com
    日期：2021/5/9
    用法：re_catch.py [option]
    option: card        获取公主链接卡面
            title_bg    获取bangbang主题背景
            ……
    P.S.每次运行后都可以覆盖更新，隔段时间运行一下就可以了，持续更新中……
"""
import sys
import os
import requests
from lxml import etree
from multiprocessing import Pool


class Catcher(object):

    def __init__(self):
        self.url_source_list = {
            'card': 'https://redive.estertion.win/card/full/',
            'title_bg': 'https://redive.estertion.win/bang/title_bg/',
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (K'
                          'HTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56'
        }
        # self.option 命令行参数
        try:
            self.option = sys.argv[1]
        except IndexError:
            self.error_response("No option, please enter option after 're_catch.py'")
        # self.url_source 目标地址
        if self.option in list(self.url_source_list.keys()):
            self.url_source = self.url_source_list[self.option]
        else:
            self.error_response("Uncorrected option, please check option you enter")

    # 创建/自动更新（迫真）文件夹
    def mkcard(self, option):
        # 如果文件夹已存在，清空文件夹（先清空后删除再创建）
        pathd = os.getcwd() + '\\%s' % option
        if os.path.exists(pathd):  # 判断文件夹是否存在
            for root, dirs, files in os.walk(pathd, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))  # 删除文件
                for name in dirs:
                    os.rmdir(os.path.join(root, name))  # 删除文件夹
            os.rmdir(pathd)  # 删除文件夹
        os.mkdir(pathd)  # 创建文件夹

    # 获取图片编号
    def get_href_card_list(self):
        response_source = requests.get(url=self.url_source, headers=self.headers)  # 请求页面
        html_source = etree.HTML(response_source.content.decode('UTF-8'))  # 实例化HTML
        href_card_list = html_source.xpath('//a//@href')  # 定位编号
        return href_card_list

    # 下载图片
    def download_card(self, href_card, path):
        url_card = self.url_source + href_card
        response_card = requests.get(url=url_card, headers=self.headers)  # 发送请求
        file_name = self.join_list(href_card)
        if response_card.status_code == 200:  # 如果请求成功
            with open(path + '/' + file_name, 'wb') as file:
                file.write(response_card.content)  # 写入图片

    def join_list(self, item):
        return ''.join(item)

    def error_response(self, error):
        print("OptionError: %s\n"
              "Syntax: re_catch.py [option]\n"
              "[option]: card        获取公主链接卡面\n\t  title_bg    获取bangbang主题背景" % error)
        exit()

    def run(self):
        self.mkcard(self.option)
        pool = Pool(processes=10)  # 创建10个进程
        href_list = self.get_href_card_list()
        for href in href_list:
            pool.apply_async(self.download_card, args=(href, self.option))
        pool.close()
        pool.join()


if __name__ == '__main__':
    cat = Catcher()
    cat.run()

