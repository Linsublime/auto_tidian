#!/usr/bin/env python
# coding=utf-8
from __future__ import division
__author__ = 'root'


import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import MySQLdb
import numpy as py
import sqlalchemy
import pandas as pd

def had_simulation(content):
    rate = rate_table[rate_table['data_id'] == data_id]
    if len(rate) != 0:
        h = float(rate['h'])
        d = float(rate['d'])
        a = float(rate['a'])
        Query = had_table.query('h==%s&d==%s&a==%s' % (h, d, a))
        odd = 'had_result'
        rate_dict = Query[odd].value_counts().to_dict()
        match_count = sum(Query[odd].value_counts().values)
        if match_count > 5:
            rate_h = rate_dict.get('3', None) / match_count if not rate_dict.get('3', None) == None else 0
            rate_d = rate_dict.get('1', None) / match_count if not rate_dict.get('1', None) == None else 0
            rate_a = rate_dict.get('0', None) / match_count if not rate_dict.get('0', None) == None else 0
            if rate_a > 0.7:
                content += '<p>' + text + u"负的概率高达%.2f%%。" % (rate_a * 100) + '</p>'
                cursor.execute("UPDATE forecast_result SET had_result=%s WHERE data_id=%s ", ('a', data_id,))
                print('<p>' + num + text + u"负的概率高达%.2f%%" % (rate_a * 100)) + '</p>'
            elif rate_d > 0.7:
                content += '<p>' + text + u"平的概率高达%.2f%%。" % (rate_d * 100) + '</p>'
                cursor.execute("UPDATE forecast_result SET had_result=%s WHERE data_id=%s ", ('d', data_id,))
                print('<p>' + num + text + u"平的概率高达%.2f%%" % (rate_d * 100)) + '</p>'
            elif rate_h > 0.7:
                content += '<p>' + text + u"胜的概率高达%.2f%%。" % (rate_h * 100) + '</p>'
                cursor.execute("UPDATE forecast_result SET had_result=%s WHERE data_id=%s ", ('h', data_id,))
                print('<p>' + num + text + u"胜的概率高达%.2f%%" % (rate_h * 100)) + '</p>'
            elif rate_a + rate_d > 0.7:
                if not (1.01 < min(a, d) < 2.0):
                    content += '<p>' + text + u"负/平的概率高达%.2f%%。" % ((rate_a + rate_d) * 100) + '</p>'
                    cursor.execute("UPDATE forecast_result SET had_result=%s WHERE data_id=%s ", ('a,d', data_id,))
                    print('<p>' + num + text + u"负/平的概率高达%.2f%%" % ((rate_a + rate_d) * 100)) + '</p>'
            elif rate_h + rate_d > 0.7:
                if not (1.01 < min(d, h) < 2.0):
                    content += '<p>' + text + u"胜/平的概率高达%.2f%%。" % ((rate_h + rate_d) * 100) + '</p>'
                    cursor.execute("UPDATE forecast_result SET had_result=%s WHERE data_id=%s ", ('d,h', data_id,))
                    print('<p>' + num + text + u"胜/平的概率高达%.2f%%" % ((rate_h + rate_d) * 100)) + '</p>'
            elif rate_a + rate_h > 0.7:
                if not (1.01 < min(a, h) < 2.0):
                    content += '<p>' + text + u"胜/负的概率高达%.2f%%。" % ((rate_a + rate_h) * 100) + '</p>'
                    cursor.execute("UPDATE forecast_result SET had_result=%s WHERE data_id=%s ", ('a,h', data_id,))
                    print('<p>' + num + text + u"胜/负的概率高达%.2f%%" % ((rate_a + rate_h) * 100)) + '</p>'
    return content


def hhad_simulation(content):
    rate = h_rate_table[h_rate_table['data_id'] == data_id]
    if len(rate) != 0:
        fixedodds = float(rate['fixedodds'])
        h = float(rate['h'])
        d = float(rate['d'])
        a = float(rate['a'])
        Query = hhad_table.query('h==%s&d==%s&a==%s&fixedodds==%s' % (h, d, a, fixedodds,))
        odd = 'hhad_result'
        rate_dict = Query[odd].value_counts().to_dict()
        match_count = sum(Query[odd].value_counts().values)
        if match_count > 5:
            rate_h = rate_dict.get('3', None) / match_count if not rate_dict.get('3', None) == None else 0
            rate_d = rate_dict.get('1', None) / match_count if not rate_dict.get('1', None) == None else 0
            rate_a = rate_dict.get('0', None) / match_count if not rate_dict.get('0', None) == None else 0
            if rate_a > 0.7:
                content += '<p>' + text + u"让球负的概率高达%.2f%%。" % (rate_a * 100) + '</p>'
                cursor.execute("UPDATE forecast_result SET hhad_result=%s WHERE data_id=%s ", ('a', data_id,))
                print('<p>' + num + text + u"让球负的概率高达%.2f%%" % (rate_a * 100)) + '</p>'
            elif rate_d > 0.7:
                content += '<p>' + text + u"让球平的概率高达%.2f%%。" % (rate_d * 100) + '</p>'
                cursor.execute("UPDATE forecast_result SET hhad_result=%s WHERE data_id=%s ", ('d', data_id,))
                print('<p>' + num + text + u"让球平的概率高达%.2f%%" % (rate_d * 100)) + '</p>'
            elif rate_h > 0.7:
                content += '<p>' + text + u"让球胜的概率高达%.2f%%。" % (rate_h * 100) + '</p>'
                cursor.execute("UPDATE forecast_result SET hhad_result=%s WHERE data_id=%s ", ('h', data_id,))
                print('<p>' + num + text + u"让球胜的概率高达%.2f%%" % (rate_h * 100)) + '</p>'
            elif rate_a + rate_d > 0.7:
                if not (1.01 < min(a, d) < 2.0):
                    content += '<p>' + text + u"让球负/平的概率高达%.2f%%。" % ((rate_a + rate_d) * 100) + '</p>'
                    cursor.execute("UPDATE forecast_result SET hhad_result=%s WHERE data_id=%s ", ('a,d', data_id,))
                    print('<p>' + num + text + u"让球负/平的概率高达%.2f%%" % ((rate_a + rate_d) * 100)) + '</p>'
            elif rate_h + rate_d > 0.7:
                if not (1.01 < min(d, h) < 2.0):
                    content += '<p>' + text + u"让球胜/平的概率高达%.2f%%。" % ((rate_h + rate_d) * 100) + '</p>'
                    cursor.execute("UPDATE forecast_result SET hhad_result=%s WHERE data_id=%s ", ('d,h', data_id,))
                    print('<p>' + num + text + u"让球胜/平的概率高达%.2f%%" % ((rate_h + rate_d) * 100)) + '</p>'
            elif rate_a + rate_h > 0.7:
                if not (1.01 < min(a, h) < 2.0):
                    content += '<p>' + text + u"让球胜/负的概率高达%.2f%%。" % ((rate_a + rate_h) * 100) + '</p>'
                    cursor.execute("UPDATE forecast_result SET hhad_result=%s WHERE data_id=%s ", ('a,h', data_id,))
                    print('<p>' + num + text + u"让球胜/负的概率高达%.2f%%" % ((rate_a + rate_h) * 100)) + '</p>'
    return content


def hafu_simulation(content):
    rate = rate_table[rate_table['data_id'] == data_id]
    if len(rate) != 0:
        h = float(rate['h'])
        d = float(rate['d'])
        a = float(rate['a'])
        Query = had_table.query('h==%s&d==%s&a==%s' % (h, d, a))
        odd = 'half_final_result'
        rate_dict = Query[odd].value_counts().to_dict()
        n_sum = sum(Query[odd].value_counts().values)
        if n_sum > 5:
            n_sum = float(n_sum)
            a_dict = {'rate_aa': u'半负全负', 'rate_ad': u'半负全平', 'rate_ah': u'半负全胜', 'rate_da': u'半平全负',
                      'rate_dd': u'半平全平', 'rate_dh': u'半平全胜', 'rate_ha': u'半胜全负', 'rate_hd': u'半胜全平',
                      'rate_hh': u'半胜全胜', }
            (rate_aa, rate_ad, rate_ah, rate_da, rate_dd, rate_dh, rate_ha, rate_hd, rate_hh,) = py.array([
                rate_dict.get('0-0', 0), rate_dict.get('0-1', 0), rate_dict.get('0-3', 0),
                rate_dict.get('1-0', 0), rate_dict.get('1-1', 0), rate_dict.get('1-3', 0),
                rate_dict.get('3-0', 0), rate_dict.get('3-1', 0), rate_dict.get('3-3', 0), ]) / n_sum
            a_rate_dict = {'rate_aa': rate_aa, 'rate_ad': rate_ad, 'rate_ah': rate_ah, 'rate_da': rate_da,
                           'rate_dd': rate_dd, 'rate_dh': rate_dh, 'rate_ha': rate_ha, 'rate_hd': rate_hd,
                           'rate_hh': rate_hh, }
            for key, value in a_rate_dict.items():
                if value > .5:
                    content += '<p>' + text + u'''%s的概率高达%.2f%%。''' % (a_dict[str(key)], value * 100) + '</p>'
                    cursor.execute("UPDATE forecast_result SET half_final_result=%s WHERE data_id=%s ", (str(key)[-2:], data_id,))
                    print('<p>' + num + text + u'''%s的概率高达%.2f%%''' % (a_dict[str(key)], value * 100)) + '</p>'
    return content


def ttg_simulation(content):
    rate = rate_table[rate_table['data_id'] == data_id]
    if len(rate) != 0:
        h = float(rate['h'])
        d = float(rate['d'])
        a = float(rate['a'])
        Query = had_table.query('h==%s&d==%s&a==%s' % (h, d, a))
        odd = 'final_count'
        rate_dict = Query[odd].value_counts().to_dict()
        n_sum = sum(Query[odd].value_counts().values)
        if n_sum > 5:
            n_sum = float(n_sum)
            (rate_0, rate_1, rate_2, rate_3, rate_4, rate_5, rate_6, rate_7,) = py.array(
                [rate_dict.get('0', 0), rate_dict.get('1', 0), rate_dict.get('2', 0), rate_dict.get('3', 0),
                 rate_dict.get('4', 0), rate_dict.get('5', 0), rate_dict.get('6', 0), rate_dict.get('7+', 0), ]) / n_sum
            a_dict = {'0': rate_0, '1': rate_1, '2': rate_2, '3': rate_3,
                      '4': rate_4, '5': rate_5, '6': rate_6, '7+': rate_7, }
            a_list = sorted(a_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
            rate = 0
            count_text = ''
            for t in a_list:
                rate += t[1]
                count_text += t[0]
                if rate > .5:
                    content += '<p>' + text + u'''总进球数为%s的概率高达%.2f%%。''' % (count_text, rate * 100) + '</p>'
                    cursor.execute("UPDATE forecast_result SET final_count=%s WHERE data_id=%s ", (count_text, data_id,))
                    print('<p>' + num + text + u'''总进球数为%s的概率高达%.2f%%.''' % (count_text, rate * 100)) + '</p>'
                    break
                count_text += '/'
    return content


# text = u'  按照爱竞彩的初盘统计系统，在相似竞彩奖金的情况下，本场比赛'
text = u'爱竞彩初盘统计'
conn = MySQLdb.connect('192.168.100.2', 'root', 'root', 'oddsfair', charset="utf8")
cursor = conn.cursor()

engine = sqlalchemy.create_engine('mysql://root:root@192.168.100.2/?charset=utf8')
match_table = pd.read_sql(
    u"SELECT data_id,num,date FROM oddsfair.sporttery_baseinfo WHERE (date = Date(now()) AND time>Time(now())) "
    "OR date > Date(now()) ORDER BY data_id", engine, )
rate_table = pd.read_sql(u"SELECT * FROM oddsfair.c", engine, )
h_rate_table = pd.read_sql(u"SELECT * FROM oddsfair.d", engine, )
had_table = pd.read_sql(u"SELECT * FROM oddsfair.b", engine, )
hhad_table = pd.read_sql(u"SELECT * FROM oddsfair.e", engine, )
for i in xrange(len(match_table)):
    data_id = int(match_table.iloc[i]['data_id'])
    num = str(match_table.iloc[i]['num'])
    date = str(match_table.iloc[i]['date'])
    cursor.execute("INSERT INTO forecast_result (data_id) VALUES (%s)", (data_id,))
    content = ''
    content = had_simulation(content)
    content = hhad_simulation(content)
    content = hafu_simulation(content)
    content = ttg_simulation(content)
    cursor.execute("SELECT content9 FROM tidian WHERE data_id = %s", (data_id,))
    tmp = cursor.fetchone()
    if content != '':
        if not tmp:
            cursor.execute(
              "INSERT INTO tidian (data_id,num,date,tidianType9,content9,Team9,createUser,tidianStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
              (data_id, num, date, '1', content, '1', '3', '4'))
            conn.commit()
        elif not tmp[0]:
            cursor.execute("UPDATE tidian SET content9=%s,tidianType9=1,Team9=1 WHERE data_id=%s ", (content, data_id,))
            conn.commit()
    else:
        conn.rollback()
conn.close()
