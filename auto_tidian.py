#!/usr/bin/env python
# coding=utf-8

from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from mongoengine.context_managers import switch_db
import MySQLdb
import sqlalchemy
import pandas as pd

from models import *

# DB_USER = os.environ['DB_USER']
# DB_PASS = os.environ['DB_PASS']
DB_USER = 'root'
DB_PASS = 'root'

DATABASES = {
    'default': {
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': '192.168.0.43',
        # 'HOST': 'mysql.master.localdomain',
        'PORT': '3306',
    },
}

class Simulation(object):
    def __init__(self, cursor, engine, text=None):
        self.cursor = cursor
        self.engine = engine
        self.text = text if text else u'爱竞彩初盘统计'
        self._read_sql()
        self.result_dict = {'had': {'0': u'负', '1': u'平', '3': u'胜',
                                    '0/1': u'平/负', '0/3': u'胜/负', '1/3': u'胜/平', },
                            'hafu': {'0-0': u'半负全负', '0-1': u'半负全平', '0-3': u'半负全胜',
                                     '1-0': u'半平全负', '1-1': u'半平全平', '1-3': u'半平全胜',
                                     '3-0': u'半胜全负', '3-1': u'半胜全平', '3-3': u'半胜全胜', }, }
        self.char_dict = {'hafu':{'0-0': u'aa', '0-1': u'ad', '0-3': u'ah',
                                  '1-0': u'da', '1-1': u'dd', '1-3': u'dh',
                                  '3-0': u'ha', '3-1': u'hd', '3-3': u'hh', },
                          'had': {'0': 'a', '1': 'd', '3': 'h',
                                  '0/1': 'a,d', '0/3': 'a,h', '1/3': 'd,h', }, }
    def _read_sql(self):
        self.rate_table = pd.read_sql(u"SELECT * FROM oddsfair.c", self.engine, )
        self.h_rate_table = pd.read_sql(u"SELECT * FROM oddsfair.d", self.engine, )
        self.had_table = pd.read_sql(u"SELECT * FROM oddsfair.b", self.engine, )
        self.hhad_table = pd.read_sql(u"SELECT * FROM oddsfair.e", self.engine, )

    def simulation(self, data_id, num):
        ''' 提点生成的接口，接收一个比赛记录的 data_id 和 num 作为参数，返回提点内容
        data_id: 用于查询本场比赛相关数据
        num: 用于打印输出信息
        '''
        self.content = ''
        self.data_id = data_id
        self.num = num
        self._simulation()
        self._simulation(is_hhad=True)
        return self.content

    def _simulation(self, is_hhad=False):
        rate_table = self.h_rate_table if is_hhad else self.rate_table
        rate = rate_table[rate_table['data_id'] == self.data_id]
        if len(rate) != 0:
            h = float(rate['h'])
            d = float(rate['d'])
            a = float(rate['a'])
            if is_hhad:
                fixedodds = float(rate['fixedodds'])
                self.Query = self.hhad_table.query('h==%s&d==%s&a==%s&fixedodds==%s' % (h, d, a, fixedodds,))
            else:
                self.Query = self.had_table.query('h==%s&d==%s&a==%s' % (h, d, a))
            n_sum = sum(self.Query['had_result'].value_counts().values)
            if n_sum > 5:
                self.n_sum = float(n_sum)
                if is_hhad:
                    self._had(h, d, a, is_hhad=True)
                else:
                    self._had(h, d, a, is_hhad=False)
                    self._hafu()
                    self._ttg()

    def _had(self, h, d, a, is_hhad=False):
        odd = 'hhad_result' if is_hhad else 'had_result'
        rate_dict = self._get_rate_dict(odd=odd, is_ordered=True)
        rate_dict['0/1'] = rate_dict.get('0', 0) + rate_dict.get('1', 0)
        rate_dict['0/3'] = rate_dict.get('0', 0) + rate_dict.get('3', 0)
        rate_dict['1/3'] = rate_dict.get('1', 0) + rate_dict.get('3', 0)
        for key, value in rate_dict.items():
            if value > 0.7:
                if len(key) > 1:
                    x1, x2 = [locals()[char] for char in self.char_dict['had'][key].split(',')]
                    if (1.01 < min(x1, x2) < 2.0):
                        continue
                result_str = u'让球' + self.result_dict['had'][key] if is_hhad else self.result_dict['had'][key]
                self.content += u"<p>%s:%s的概率高达%.2f%%。</p>" % (self.text, result_str, value * 100)
                if is_hhad:
                    cursor.execute("UPDATE forecast_result SET hhad_result=%s WHERE data_id=%s ", (self.char_dict['had'][key], self.data_id,))
                else:
                    cursor.execute("UPDATE forecast_result SET had_result=%s WHERE data_id=%s ", (self.char_dict['had'][key], self.data_id,))
                print(u"<p>%s:%s的概率高达%.2f%%。</p>" % (self.num + self.text, result_str, value * 100))
                break

    def _hafu(self):
        rate_dict = self._get_rate_dict(odd='half_final_result')
        rates = sorted(rate_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        # 只需判断最高概率的一项即可
        key, value = rates[0]
        if value > .5:
            self.content += u"<p>%s:%s的概率高达%.2f%%。</p>"% (self.text, self.result_dict['hafu'][key], value * 100)
            cursor.execute("UPDATE forecast_result SET half_final_result=%s WHERE data_id=%s ",
                           (self.char_dict['hafu'][key], self.data_id,))
            print(u"<p>%s:%s的概率高达%.2f%%。</p>"% (self.num + self.text, self.result_dict['hafu'][key], value * 100))

    def _ttg(self):
        rate_dict = self._get_rate_dict(odd='final_count')
        a_list = sorted(rate_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        rate = 0
        count_text = ''
        for key, value in a_list:
            count_text += key
            rate += value
            if rate > .5:
                self.content += u"<p>%s:总进球数为%s的概率高达%.2f%%。</p>"% (self.text, count_text, rate * 100)
                cursor.execute("UPDATE forecast_result SET final_count=%s WHERE data_id=%s ", (count_text, self.data_id,))
                print(u"<p>%s:总进球数为%s的概率高达%.2f%%。</p>"% (self.num + self.text, count_text, rate * 100))
                break
            count_text += '/'

    def _get_rate_dict(self, odd, is_ordered=False):
        tmp = self.Query[odd].value_counts().to_dict()
        rate_dict = OrderedDict() if is_ordered else {}
        for k, v in tmp.items():
            rate_dict[k] = v / self.n_sum
        return rate_dict

if __name__ == '__main__':
    # text = u'  按照爱竞彩的初盘统计系统，在相似竞彩奖金的情况下，本场比赛'
    # conn = MySQLdb.connect('mysql.master.localdomain', DB_USER, DB_PASS, "oddsfair", charset="utf8")
    # conn = MySQLdb.connect('mysql.master.localdomain', DB_USER, DB_PASS, "oddsfair", charset="utf8")
    conn = MySQLdb.connect('192.168.0.43', DB_USER, DB_PASS, "oddsfair", charset="utf8")
    cursor = conn.cursor()
    engine = sqlalchemy.create_engine('mysql://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/?charset=utf8' % (DATABASES['default']),)
    match_table = pd.read_sql(
        u"SELECT data_id,num,date FROM oddsfair.sporttery_baseinfo WHERE (date = Date(now()) AND time>Time(now())) "
        "OR date > Date(now()) ORDER BY data_id", engine, )
    simulation = Simulation(cursor=cursor, engine=engine)

    for i in xrange(len(match_table)):
        data_id = int(match_table.iloc[i]['data_id'])
        num = str(match_table.iloc[i]['num'])
        date = str(match_table.iloc[i]['date'])
        cursor.execute("INSERT INTO forecast_result (data_id) VALUES (%s)", (data_id,))
        content = simulation.simulation(data_id=data_id, num=num)
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
            if (not tmp) or (not tmp[0]):
                # mongo 数据保存
                with switch_db(TidianContent, db_alias='od') as tdc:
                    t = tdc.objects(data_id=data_id).first()
                    if not t:
                        t = tdc(data_id=data_id, contents=TdContents())
                    t.contents.type1 = content
                    t.save()
        else:
            conn.rollback()
    conn.close()
    mgdb.close()