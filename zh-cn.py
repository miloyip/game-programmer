# -*- coding:utf8 -*-
"""
读取game-programmer.dot将其转换为中文版的game-programmer-zh-cn.dot
"""
import json
import re
import urllib2
import csv
import os

IMAGE_PATH = './images-zh-cn/{book_index}.jpg'

def get_image(isbn, image_filename):
    """
    :type en_isbn: str
    :rtype: str
    """
    print("get_image(" + isbn + "," + isbn + ")")
    response = urllib2.urlopen(book_url)
    html = response.read()
    re_image_url = r"https://img\d\.doubanio\.com/lpic/s\d*\.jpg"
    image_url = re.search(re_image_url, html).group()
    with open(image_filename, 'w') as ft:
        response = urllib2.urlopen(image_url)
        image = response.read()
        ft.write(image)

def get_book_url_year(isbn):
    print("get_book_url_year(" + isbn + ")")
    url = "https://api.douban.com/v2/book/isbn/" + isbn
    result = "https://book.douban.com/", ""
    try:
        response = urllib2.urlopen(url)
        detail = response.read()
        return json.loads(detail)["alt"], json.loads(detail)["pubdate"][:4]
    except Exception as e:
        print isbn
        print e
        return result

def get_book_info(book_index):
    print("get_book_info(" + book_index + ")")
    title = "未找到中文"
    zh_isbn = ""
    with open("isbn.csv") as ff:
        spamreader = csv.reader(ff, delimiter=',')
        for line in spamreader:
            if line[0] == book_index:
                title = line[2].strip()
                zh_isbn = line[3]
    if title == "未找到中文":
        return None, None, None
    else:
        image_path = IMAGE_PATH.format(book_index=book_index.strip('"'))

        if not os.path.exists(image_path):
            get_image(zh_isbn, image_path)
        book_url, book_year = get_book_url_year(zh_isbn)
        return title, book_url, book_year

LABEL_DICT = {
    "":"",
    "Recommended Path": "推荐路线",
    "Optional Path": "可选路线",
    "Beginning from Age of 5": "从5岁开始",
    "Beginning from Age of 8": "从8岁开始",
    "Intermediate Game Programming for Kids": "中级孩童游戏编程",
    "CS Foundation": "计算机基础",
    "Algorithm": "算法",
    "Mathematics for CS": "计算机数学",
    "C": "C",
    "Lua": "Lua",
    "C#": "C#",
    "Beginning C++": "C++ 新手",
    "C++ Practice": "C++ 实践",
    "C++ Standard Library": "C++ 标准库",
    "Advanced C++": "C++ 进阶",
    "Beginning Software Development": "软件开发新手",
    "Practice": "实践",
    "Design Pattern": "设计模式",
    "UML": "UML",
    "Beginning Mathematics for Game Programming": "游戏编程数学初阶",
    "Advanced Mathematics for Game Programming": "游戏编程数学进阶",
    "Beginning Game Programming": "开始游戏编程",
    "From Windows/DirectX": "使用Windows/DirectX",
    "From Unity": "使用Unity",
    "From Unreal": "使用Unreal",
    "From Cocos2d-X": "使用Cocos2d-X",
    "Intermediate Game Programming": "中级游戏编程",
    "Game Programming Articles": "游戏编程文选",
    "Beginning Game Engine Development": "游戏引擎开发新手",
    "Game Engine Articles": "游戏引擎文选",
    "Script Engine": "脚本引擎",
    "Optimization": "优化",
    "Tool Development": "工具开发",
    "Beginning CG Programming": "游戏图形学初级",
    "Beginning CG theory": "图形学理论初级",
    "Advanced CG": "图形学进阶",
    "Real-Time Rendering": "实时渲染",
    "Offline Rendering": "离线渲染",
    "Direct3D": "Direct3D",
    "OpenGL": "OpenGL",
    "CG Technologies": "图形学技术",
    "CG Articles": "图形学文选",
    "Game Audio Programming": "游戏音频编程",
    "Beginning Game Animation Programming": "游戏动画初阶",
    "Advanced Game Animation Programming": "游戏动画进阶",
    "Beginning Game Physics Programming": "游戏物理初阶",
    "Advanced Game Physics Programming": "游戏物理进阶",
    "Fluid Animation/Simulation": "流体动画/模拟",
    "Beginning Game AI": "游戏AI初阶",
    "Intermediate Game AI": "中级游戏AI",
    "Game AI Articles": "游戏AI文选",
    "Beginning Multiplayer Game Programming": "多人游戏编程初阶",
    "Multiplayer Game Articles": "多人游戏编程文选",
    "Server Programming": "服务器编程",
    "Network Protocol": "网络协议",
    "Network Programming": "网络编程",
}

SECTION_TITLE_DICT = {
    "0.": "0. 编程学前班",
    "1.": "1. 计算机科学",
    "2.": "2. 编程语言",
    "3.": "3. 软件开发",
    "4.": "4. 游戏程序员的数学课",
    "5.": "5. 游戏编程",
    "6.": "6. 游戏引擎开发",
    "7.": "7. 计算机图形学（CG）",
    "8.": "8. 游戏音效",
    "9.": "9. 游戏物理和动画",
    "10.": "10. 游戏人工智能（AI）",
    "11.": "11. 多人游戏编程",
}

RE_BOOK_LINE = re.compile(r'^\"?\w*\"?\w* \[label=<<TABLE[\S ]* URL="https?:/{2}\w.+"]$')
BOOK_LINE = '{book_index} [label=<<TABLE BORDER="0" CELLSPACING="0"><TR><TD WIDTH="100" HEIGHT="100" FIXEDSIZE="TRUE"><IMG SCALE="TRUE" SRC="{image_path}"/></TD></TR><TR><TD>{book_title}<br/>({book_year})</TD></TR></TABLE>> URL="{url}"]\n'
RE_SECTION_LINE = re.compile(r'^label=<<TABLE BORDER="0" CELLPADDING="10"><TR><TD>\d+\.[\w. ()]*</TD></TR></TABLE>>$')
SECTION_LINE = 'label=<<TABLE BORDER="0" CELLPADDING="10"><TR><TD>{section_title}</TD></TR></TABLE>>\n'
RE_LABEL_LINE = re.compile(r'^\w+ \[label="[\w -=\./\\]*"\]$')
LABEL_LINE = '{label_index} [label="{label}"]\n'
RE_CONTENT_LINE = re.compile(r'[\w ]+\[color="#[\w]{6}", label=[<"]\d+\. [\w ()]+[">]\]')


if __name__ == '__main__':
    with open("game-programmer.dot") as en_f, open("game-programmer-zh-cn.dot",'w') as zh_f:
        for line in en_f:
            #==== 处理标题
            if line.strip().startswith('<TR><TD><FONT FACE="Futura" POINT-SIZE="40">A STUDY PATH FOR</FONT></TD></TR>'):
                zh_f.write('<TR><TD><FONT FACE="Futura" POINT-SIZE="40">游戏程序员的</FONT></TD></TR>')
                continue
            elif line.strip().startswith('<TR><TD><FONT FACE="Futura-Bold" POINT-SIZE="40">GAME PROGRAMMER</FONT></TD></TR>'):
                zh_f.write('<TR><TD><FONT FACE="Futura" POINT-SIZE="40">学习之路</FONT></TD></TR>')
                continue

            line_without_space = line.strip()
            space_front = line[:len(line)-len(line_without_space)-1]

            book_line_match = RE_BOOK_LINE.match(line_without_space)
            section_line_match = RE_SECTION_LINE.match(line_without_space)
            label_line_match = RE_LABEL_LINE.match(line_without_space)
            content_line_match = RE_CONTENT_LINE.match(line_without_space)

            if book_line_match != None:
                book_index = line_without_space.split(" ")[0]
                book_title, book_url, book_year = get_book_info(book_index.strip('"'))
                if book_title == None:
                    zh_f.write(line)
                else:
                    image_path = IMAGE_PATH.format(book_index=book_index.strip('"'))
                    writeline = space_front+ BOOK_LINE.format(book_index=book_index, image_path=image_path, book_title=book_title, book_year=book_year, url=book_url)
                    zh_f.write(writeline)
            elif section_line_match != None:
                sectionID = re.search(r'\d+\.', line_without_space).group()
                writeline = space_front + SECTION_LINE.format(section_title=SECTION_TITLE_DICT[sectionID])
                zh_f.write(writeline)
            elif label_line_match != None:
                label_index = label_line_match.group().split(' ')[0]
                en_label_content = re.search(r'label="[\w -=\./\\]*"', line_without_space).group()[7:-1]
                writeline = space_front + LABEL_LINE.format(label_index=label_index, label=LABEL_DICT[en_label_content])
                zh_f.write(writeline)
            elif content_line_match != None:
                sectionID = line_without_space.split('.')[0][37:] + '.'
                section_title =SECTION_TITLE_DICT[sectionID]
                if '<' in line_without_space:
                    writeline = space_front + line_without_space.split('.')[0][:37] + ' ' + section_title + '>]\n'
                elif '"' in line_without_space:
                    writeline = space_front + line_without_space.split('.')[0][:37] + ' ' + section_title + '"]\n'
                else:
                    writeline = line
                zh_f.write(writeline)
            else:
                zh_f.write(line)
