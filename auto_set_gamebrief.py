# coding=utf-8
__author__ = 'yuxiaorui'
import os

from mongoengine.context_managers import switch_db
import MySQLdb

from models import *

DB_USER = 'root'
DB_PASS = 'root'

db = MySQLdb.connect('192.168.0.43', DB_USER, DB_PASS, "oddsfair", charset="utf8")
tx = db.cursor(MySQLdb.cursors.DictCursor)
# tx.execute("select * from tidian where data_id = 70413 ")
tx.execute("select * from tidian where date > Date(now()) AND (gamebrief = '' or isnull(gamebrief))")
result = tx.fetchall()
data_id_list = [ x.get('data_id') for x in result ]
with switch_db(TidianContent, db_alias='od') as tdc:
    mongo_result = tdc.objects(data_id__in=data_id_list)
for item, mongo_item in zip(result, mongo_result):
    test_key = [k for k, v in item.iteritems() if (v in (9,2,8))&('tidianType' in k)]
    if test_key:
        gamebrief = item.get('gamebrief')
        gamebrief = gamebrief if gamebrief != None else ''
        for i in xrange(1, 11):
            num = gamebrief.count('<p')
            if num < 3:
                content = item.get('content' + str(i))
                if content != None:
                    gamebrief = gamebrief + content
                    num = gamebrief.count('<p')
                    if num >= 3:
                        tx.execute("update tidian set gamebrief = %s WHERE data_id = %s", (gamebrief, item.get('data_id')))
                        db.commit()
                        mongo_item.contents.gamebrief = gamebrief
                        mongo_item.save()
                        break
db.close()
mgdb.close()