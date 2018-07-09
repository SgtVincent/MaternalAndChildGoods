# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3 
import requests

class MaternalandchildgoodsPipeline(object):


    def open_spider(self, spider):
        # We should connect to the database before we begin our spider
        self.conn = sqlite3.connect("./database.db")
        self.cursor = self.conn.cursor()
        self.commit_cnt = 0

        # Create sqlite tables for texts and images separately
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS
            Text(
                time DATETIME,
                text TEXT,
                topic TEXT
            );
        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS
            Image(
                time DATETIME,
                src TEXT,
                title TEXT,
                bin TEXT
            );
        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS
            Topic(
                time DATETIME,
                text TEXT,
                href TEXT,
                view_cnt INT,
                reply_cnt INT,
                tag TEXT
            );
        ''')

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        
        # process Text item
        if item['cls_tag'] == 0: 
            insert_sql = "INSERT INTO Text VALUES (?,?,?)"
            # time, text, topic
            insert_values = [
                item.get('time'),
                item.get('text'),
                item.get('topic')
            ]
            self.cursor.execute(insert_sql,insert_values)
        
        # process ImageUrl item
        elif item['cls_tag'] == 1:
            try:
                # First, we retrieve the binary of the image
                headers = {
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                }
                url = item['src']
                # handle corner case like "//baidu.com" 
                if not url.startswith('http'):
                    url = 'http:'+url

                request = requests.get(item['src'], headers=headers)
                
                insert_sql = "INSERT INTO Image VALUES (?,?,?,?)"
                # time, src, title, bin

                insert_values = [
                    item.get('time'),
                    item.get('src'),
                    item.get('title'),
                    request.content
                ]
                # insert values into DB
                self.cursor.execute(insert_sql,insert_values)
            except Exception as e:
                print(e)
                print("Error in processing ImageUrl item")

        elif item['cls_tag'] == 2:
            insert_sql = "INSERT INTO Topic VALUES(?,?,?,?,?,?)"
            # time, text, href, view_cnt, reply_cnt, tag
            insert_values = [
                item.get('time'),
                item.get('text'),
                item.get('href'),
                item.get('view_cnt'),
                item.get('reply_cnt'),
                item.get('tag')
            ]
            self.cursor.execute(insert_sql,insert_values)

        else :
            print("Unknown item type tag: ", item['cls_tag'])

        return item
 