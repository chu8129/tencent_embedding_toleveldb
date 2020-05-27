#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create By qiuwen(mail:chu8129@gmail.com) @ 2020-05-12 18:42:44
# Last Modified : 2020-05-27 10:57:37,3

# 原因：加载原始的txt，时间，内存，都是问题
# 将腾讯的w2v转换成leveldb
# 转成mysql也可以，但是需要关注key的大小，腾讯的还是挺乱的
# unqlite，本来是想转换成单一文件的形式，但是这货内存消耗
# 与fasttext对比，腾讯的词稍微全一点，但相对的也会比较乱
# link:https://ai.tencent.com/ailab/nlp/data/Tencent_AILab_ChineseEmbedding.tar.gz

import logging
logger = logging.getLogger("root")

import leveldb

class Vector2Write(object):

    def write(self):
        filename = "/ssd/Tencent_AILab_ChineseEmbedding.txt"
        db = leveldb.LevelDB(filename + ".leveldb")
        try:
            print(db.Get("皓影".encode()).decode().split(","))
        except Exception as e:
            print(e)
        count = 0
        with open(filename) as fr:
            for line in fr:
                count += 1
                split_line = line.strip().split(" ")
                word = split_line[0].strip().replace("\t", " ").replace("\r", " ")
                vector = ",".join(split_line[1:])
                db.Put(word.encode(),vector.encode())


if __name__ == "__main__":
    Vector2Write().write()

"""
入库mysql需要注意一个key:\
写文件的形式再load table

mysql> use embedding
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show create table tencent;
+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table   | Create Table                                                                                                                                                |
+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tencent | CREATE TABLE `tencent` (
  `word` varchar(1024) NOT NULL,
  `vector` varchar(2048) DEFAULT NULL,
    unique KEY (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 |
+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
load data local infile '/ssd/Tencent_AILab_ChineseEmbedding.txt.forloaddata' replace into table tencent fields terminated by '\t' (word, vector);
"""
