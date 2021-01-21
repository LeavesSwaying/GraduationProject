# -*- coding = utf-8 -*-
# @Time : 2021/1/21
# @Author : imchenio
# @File: mongodb.py
# @Software: PyCharm

import pymongo
#练习：将Movielens数据集写入mongodb数据库
def ProcessDataFile():
    fp=open("ratings.dat","r")
    for line in fp:
        yield line.strip("\r\n")

def ProcessDataBase():
    myclient=pymongo.MongoClient("mongodb://localhost:27017/")
    mydb=myclient["MovieLens"]
    mycol=mydb["ratings"]
    for i,line in enumerate(ProcessDataFile()):
        user,movie,rating,_ = line.split("::")
        mydoc={"uid":i,"用户":user,"电影":movie,"分数":rating}
        mycol.insert_one(mydoc)
        print(i)

if __name__=="__main__":
    ProcessDataBase()