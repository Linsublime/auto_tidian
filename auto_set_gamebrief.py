# coding=utf-8
__author__ = 'yuxiaorui'
import MySQLdb

db = MySQLdb.connect(
    host='localhost',
    db='oddsfair',
    user='root',
    passwd='',
    charset='utf8', )
tx = db.cursor(MySQLdb.cursors.DictCursor)
# tx.execute("select * from tidian where data_id = 70413 ")
tx.execute("select * from tidian where gamebrief = '' or isnull(gamebrief)")
result = tx.fetchall()
for item in result:
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
                    break
db.close()
