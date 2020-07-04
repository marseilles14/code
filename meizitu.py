#coding: utf-8
import urllib.request as req
import re
import urllib.error as err
import os
import socket
#socket.setdefaulttimeout(10)
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
regx = 'https:\/\/5252ll\.com/luyilu/201\d{1}/.+?\.html'#图片页
regx1 = 'class=\'next-page\''#下一页按钮
regx3 = 'https:\/\/www\.images\.zhaofulipic\.com:8819\/allimg/\d{6}\/.+?\.jpg'#每张图片
#https://www.images.zhaofulipic.com:8819/allimg/171022/1A9102G4-98.jpg
regx4 = '<h1 class="article-title">.*?]'

page_pic_list_regx='<article class="article-content">[\S\s]+?</article>'

disk='E:\\'
#获取页面代码
def url_req(url,header):
    reqs = req.Request(url, headers=header)
    resp = req.urlopen(reqs,timeout=0.001)
    file = resp.read().decode('utf-8')
    return file
#创造文件夹
def make_dir(page):
    rr = re.compile(regx4)
    t=get_tit(page)
    print(t)
    path = disk + 'pic_meizi\\' + str(t)
    print(path)
    if os.path.exists(path):
        os.chdir(path)
    else:
        os.makedirs(path)
        os.chdir(path)

def get_tit(page):
    titles = re.findall(regx4, page)  # 每一个group的name
    til = re.split('">', str(titles))
    tit = re.split("'", str(til[1]))
    return tit[0]

def down_pic(j,k):
    try:
        s=1
        req.urlretrieve(j, k)
        print(k)
    except err.ContentTooShortError as e:#图片在特定时间内没有下载完成
        print('chongxinqingqiu')
        dwon_pic(j, k)
    except socket.timeout:
        s=s+1
        if s<10:
            print('超时')
            down_pic(j,k)
        else:
            print('跳过本张图片')
    except err.URLError:
        s=s + 1
        if s < 10:
            print('URL错误')
            down_pic(j, k)
        else:
            print('跳过本张图')
    except Exception:
        print('跳过本张图')



if __name__ == '__main__':
    url = 'https://sozfl.com/serch.php?keyword=%C8%AB%B2%CA'
    try:
        file = url_req(url,header)
    except err.HTTPError as e:
        print('network mistake: %s', e)
        print('wangluocuowu')
        exit()
    except Exception as e:
        print(e)
        exit()
    lists = re.findall(regx, file)#group的列表
    list = list(set(lists))
    print('list')
    print(list)

    for i in list:
        page = url_req(i,header)#每组的第一页
        #print(page)
        t=get_tit(page)
        print('i:'+i)
        a = re.split('\.',i)
        pre=a[0]+'.'+a[1]
        print('pre'+pre)
        pag_num = 1
        make_dir(page)
        #第一页图片下载
        #第一页图片的url: https://5252ll.com/luyilu/2018/0622/5367.html
        k=1
        while(i):#循环遍历每组图片
            artical=re.findall(page_pic_list_regx,page)
            ask=str(artical[0])#在html页面中找到主体部分，可以让正则匹配更准确
            #print(ask)
            list2 = re.findall(regx3,ask)#找到本页的图片
            for j in list2:
                pic_name = t+str(k)+'.jpg'#拼保存到本地图片的名字
                k=k+1
                down_pic(j,pic_name) #将图片保存到本地
            next = re.findall(regx1, page) #看看页面是否有下一页按钮
            if next:#如果有下一页，页数+1，继续访问下一页
                pag_num = pag_num +1

                b = pre + '_' + str(pag_num) + '.' + 'html'
                print(b)
                page = url_req(b, header)
            else:#否则本组图片爬完，开始下一组
                    print('group finish')
                    i=[]
    print('finish')





        




