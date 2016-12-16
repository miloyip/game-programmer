# -*- coding:utf8 -*-
"""
获取douban上某书籍的封面图片
"""

import re
import urllib2
import csv

IMAGE_PATH = "./images-zh-cn/"

def get_image_from_douban(book_url, image_filename):
    print book_url
    response = urllib2.urlopen(book_url)
    html = response.read()
    re_image_url = r"https://img\d\.doubanio\.com/lpic/s\d*\.jpg"
    image_url = re.search(re_image_url, html).group()
    with open(image_filename, 'w') as ft:
        response = urllib2.urlopen(image_url)
        image = response.read()
        ft.write(image)

if __name__ == '__main__':
    with open("zh-cn.csv", 'r') as ff:
        spamreader = csv.reader(ff, delimiter=',')
        for line in spamreader:
            print line
            indexString, _, _, _, _, _, douban_url = line
            if re.match(r'^https?:/{2}\w.+$', douban_url):
                image_filename = IMAGE_PATH + indexString + ".jpg"
                get_image_from_douban(douban_url, image_filename)
