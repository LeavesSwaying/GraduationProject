# -*- coding = utf-8 -*-
# @Time : 2021/1/11
# @Author : imchenio
# @File: Spider.py
# @Software: PyCharm

from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import sqlite3

#影片链接
findlink=re.compile(r'<a href="(.*?)">')
#影片图片
findImgSrc=re.compile(r'<img.*src="(.*?)"',re.S)
#影片片名
findTitle=re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findJudge=re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq=re.compile(r'<span class="inq">(.*)</span>')
#相关内容
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)

def main():
    baseurl="https://movie.douban.com/top250?start="
    #爬取网页
    dataList=getData(baseurl)
    for i in range(len(dataList)):
        print(dataList[i])
    #保存数据在Excel
    #savePath=r'.\\豆瓣电影Top250.xls'
    dbPath=r'.\\豆瓣电影Top250.db'
    saveDataDB(dataList,dbPath)
    #html=askURL(baseurl)

def getData(baseurl):
    datalist=[]
    for i in range(0,10):
        url=baseurl+str(i*25)
        html=askURL(url)
        #逐一解析数据
        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            #print(item)    #测试
            data=[]         #保存一部电影的所有信息
            item=str(item)

            link=re.findall(findlink,item)[0]
            data.append(link)

            imgSrc=re.findall(findImgSrc,item)[0]
            data.append(imgSrc)

            titles=re.findall(findTitle,item)
            if(len(titles)==2):
                ctitle=titles[0]
                otitle=titles[1].replace("/","")
                data.append(ctitle)
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')

            rating=re.findall(findRating,item)[0]
            data.append(rating)

            judgeNum=re.findall(findJudge,item)[0]
            data.append(judgeNum)

            inq=re.findall(findInq,item)
            if len(inq) != 0:
                inq=inq[0].replace("。","")
                data.append(inq)
            else: data.append(" ")

            bd=re.findall(findBd,item)[0]
            bd=re.sub('<br(\s+)?/>(\s+)?'," ",bd)
            bd=re.sub("/"," ",bd)
            data.append(bd.strip())

            datalist.append(data)

    return datalist

#得到一个指定URL的网页信息
def askURL(url):
    head={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"}
    #用户代理用于告诉豆瓣服务器我们是什么类型的机器，浏览器（本质上是告诉我们可以接受什么水平的信息
    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def saveData(datalist,dbpath):
    book=xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet=book.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)
    col=('电影详情链接',"图片链接","中文名","外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save('student.xls')

def saveDataDB(datalist,dbpath):
    init_db(dbpath)
    conn=sqlite3.connect(dbpath)
    cur=conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index==4 or index==5:
                continue
            data[index] = '"'+data[index]+'"'
        sql='''
            insert into movie250(
                info_link,pic_link,cname,ename,score,rated,instroduction,info)
            values(%s)'''%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def init_db(dbpath):
    sql='''
        create table movie250
        (
            id integer primary key autoincrement,
            info_link text,
            pic_link text,
            cname varchar,
            ename varchar,
            score numeric ,
            rated numeric ,
            instroduction text,
            info text
        )
    '''
    conn=sqlite3.connect(dbpath)
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__=="__main__":
    main()
