# coding=utf-8
__author__ = 'root'
import sys
import MySQLdb
import numpy as py
reload(sys)
sys.setdefaultencoding( "utf-8" )

def had_simulation(content):
    cursor.execute("SELECT * FROM c WHERE data_id = %s", result[i][1])
    tmp = cursor.fetchone()
    if tmp:
        a = tmp[3]
        d = tmp[4]
        h = tmp[5]
        cursor.execute('SELECT had_result, count(had_result) as c1 FROM b WHERE\n'
                       ' a = %s AND d = %s AND h = %s GROUP BY had_result', (a, d, h,))
        tmp = cursor.fetchall()
        if tmp:
            tmp = dict(tmp)
            n_sum = sum([tmp.get('0', 0), tmp.get('1', 0), tmp.get('3', 0)])
            if n_sum > 5:
                n_sum = float(n_sum)
                rate_a = tmp.get('0', 0) / n_sum
                rate_d = tmp.get('1', 0) / n_sum
                rate_h = tmp.get('3', 0) / n_sum
                if rate_a > 0.7:
                    content += '<p>' + text + u"负的概率高达%.2f%%。" % (rate_a * 100) + '</p>'
                    print('<p>' + result[i][9] + text + u"负的概率高达%.2f%%" % (rate_a * 100)) + '</p>'
                elif rate_d > 0.7:
                    content += '<p>' + text + u"平的概率高达%.2f%%。" % (rate_d * 100) + '</p>'
                    print('<p>' + result[i][9] + text + u"平的概率高达%.2f%%" % (rate_d * 100)) + '</p>'
                elif rate_h > 0.7:
                    content += '<p>' + text + u"胜的概率高达%.2f%%。" % (rate_h * 100) + '</p>'
                    print('<p>' + result[i][9] + text + u"胜的概率高达%.2f%%" % (rate_h * 100)) + '</p>'
                elif rate_a + rate_d > 0.7:
                    if not (1.01 < min(a, d) < 2.0):
                        content += '<p>' + text + u"负/平的概率高达%.2f%%。" % ((rate_a + rate_d) * 100) + '</p>'
                        print('<p>' + result[i][9] + text + u"负/平的概率高达%.2f%%" % ((rate_a + rate_d) * 100)) + '</p>'
                elif rate_h + rate_d > 0.7:
                    if not (1.01 < min(d, h) < 2.0):
                        content += '<p>' + text + u"胜/平的概率高达%.2f%%。" % ((rate_h + rate_d) * 100) + '</p>'
                        print('<p>' + result[i][9] + text + u"胜/平的概率高达%.2f%%" % ((rate_h + rate_d) * 100)) + '</p>'
                elif rate_a + rate_h > 0.7:
                    if not (1.01 < min(a, h) < 2.0):
                        content += '<p>' + text + u"胜/负的概率高达%.2f%%。" % ((rate_a + rate_h) * 100) + '</p>'
                        print('<p>' + result[i][9] + text + u"胜/负的概率高达%.2f%%" % ((rate_a + rate_h) * 100)) + '</p>'
    return content


def hhad_simulation(content):
    cursor.execute("SELECT * FROM d WHERE data_id = %s", result[i][1])
    tmp = cursor.fetchone()
    if tmp:
        fixedodds = tmp[2]
        a = tmp[3]
        d = tmp[4]
        h = tmp[5]
        cursor.execute('SELECT hhad_result, count(hhad_result) as c1 FROM e WHERE\n'
                       ' a = %s AND d = %s AND h = %s AND fixedodds=%s GROUP BY hhad_result', (a, d, h, fixedodds))
        tmp = cursor.fetchall()
        if tmp:
            tmp = dict(tmp)
            n_sum = sum([tmp.get('0', 0), tmp.get('1', 0), tmp.get('3', 0)])
            if n_sum > 5:
                n_sum = float(n_sum)
                rate_a = tmp.get('0', 0) / n_sum
                rate_d = tmp.get('1', 0) / n_sum
                rate_h = tmp.get('3', 0) / n_sum
                if rate_a > 0.7:
                    content += '<p>' + text + u"让球负的概率高达%.2f%%。" % (rate_a * 100) + '</p>'
                    print('<p>' + result[i][9] + text + u"让球负的概率高达%.2f%%" % (rate_a * 100)) + '</p>'
                elif rate_d > 0.7:
                    content += '<p>' + text + u"让球平的概率高达%.2f%%。" % (rate_d * 100) + '</p>'
                    print('<p>' + result[i][9] + text + u"让球平的概率高达%.2f%%" % (rate_d * 100)) + '</p>'
                elif rate_h > 0.7:
                    content += '<p>' + text + u"让球胜的概率高达%.2f%%。" % (rate_h * 100) + '</p>'
                    print('<p>' + result[i][9] + text + u"让球胜的概率高达%.2f%%" % (rate_h * 100)) + '</p>'
                elif rate_a + rate_d > 0.7:
                    if not (1.01 < min(a, d) < 2.0):
                        content += '<p>' + text + u"让球负/平的概率高达%.2f%%。" % ((rate_a + rate_d) * 100) + '</p>'
                        print('<p>' + result[i][9] + text + u"让球负/平的概率高达%.2f%%" % ((rate_a + rate_d) * 100)) + '</p>'
                elif rate_h + rate_d > 0.7:
                    if not (1.01 < min(d, h) < 2.0):
                        content += '<p>' + text + u"让球胜/平的概率高达%.2f%%。" % ((rate_h + rate_d) * 100) + '</p>'
                        print('<p>' + result[i][9] + text + u"让球胜/平的概率高达%.2f%%" % ((rate_h + rate_d) * 100)) + '</p>'
                elif rate_a + rate_h > 0.7:
                    if not (1.01 < min(a, h) < 2.0):
                        content += '<p>' + text + u"让球胜/负的概率高达%.2f%%。" % ((rate_a + rate_h) * 100) + '</p>'
                        print('<p>' + result[i][9] + text + u"让球胜/负的概率高达%.2f%%" % ((rate_a + rate_h) * 100)) + '</p>'
    return content


def hafu_simulation(content):
    cursor.execute("SELECT * FROM c WHERE data_id = %s", result[i][1])
    tmp = cursor.fetchone()
    if tmp:
        a = tmp[3]
        d = tmp[4]
        h = tmp[5]
        cursor.execute('SELECT half_final_result, count(half_final_result) as c1 FROM b WHERE\n'
                       ' a = %s AND d = %s AND h = %s GROUP BY half_final_result', (a, d, h,))
        tmp = cursor.fetchall()
        if tmp:
            tmp = dict(tmp)
            n_sum = sum([tmp.get('0-0', 0), tmp.get('0-1', 0), tmp.get('0-3', 0), tmp.get('1-1', 0), tmp.get('1-0', 0),
                         tmp.get('1-3', 0), tmp.get('3-3', 0), tmp.get('3-1', 0), tmp.get('3-0', 0)])
            if n_sum > 5:
                n_sum = float(n_sum)
                a_dict = {'rate_aa': u'半负全负', 'rate_ad': u'半负全平', 'rate_ah': u'半负全胜', 'rate_da': u'半平全负',
                          'rate_dd': u'半平全平', 'rate_dh': u'半平全胜', 'rate_ha': u'半胜全负', 'rate_hd': u'半胜全平',
                          'rate_hh': u'半胜全胜', }
                (rate_aa, rate_ad, rate_ah, rate_da, rate_dd, rate_dh, rate_ha, rate_hd, rate_hh,) = py.array([
                    tmp.get('0-0', 0), tmp.get('0-1', 0), tmp.get('0-3', 0),
                    tmp.get('1-0', 0), tmp.get('1-1', 0), tmp.get('1-3', 0),
                    tmp.get('3-0', 0), tmp.get('3-1', 0), tmp.get('3-3', 0), ]) / n_sum
                a_rate_dict = {'rate_aa': rate_aa, 'rate_ad': rate_ad, 'rate_ah': rate_ah, 'rate_da': rate_da,
                               'rate_dd': rate_dd, 'rate_dh': rate_dh, 'rate_ha': rate_ha, 'rate_hd': rate_hd,
                               'rate_hh': rate_hh, }
                for key, value in a_rate_dict.items():
                    if value > .5:
                        content += '<p>' + text + u'''%s的概率高达%.2f%%。''' % (a_dict[str(key)], value * 100) + '</p>'
                        print('<p>' + result[i][9] + text + u'''%s的概率高达%.2f%%''' % (a_dict[str(key)], value * 100)) + '</p>'
    return content


def ttg_simulation(content):
    cursor.execute("SELECT * FROM c WHERE data_id = %s", result[i][1])
    tmp = cursor.fetchone()
    if tmp:
        a = tmp[3]
        d = tmp[4]
        h = tmp[5]
        cursor.execute('SELECT final_count, count(final_count) as c1 FROM b WHERE\n'
                       ' a = %s AND d = %s AND h = %s GROUP BY final_count', (a, d, h,))
        tmp = cursor.fetchall()
        if tmp:
            tmp = dict(tmp)
            n_sum = sum([tmp.get('0', 0), tmp.get('1', 0), tmp.get('2', 0), tmp.get('3', 0),
                         tmp.get('4', 0), tmp.get('5', 0), tmp.get('6', 0), tmp.get('7+', 0), ])
            if n_sum > 5:
                n_sum = float(n_sum)
                (rate_0, rate_1, rate_2, rate_3, rate_4, rate_5, rate_6, rate_7,) = py.array(
                    [tmp.get('0', 0), tmp.get('1', 0), tmp.get('2', 0),
                     tmp.get('3', 0), tmp.get('4', 0), tmp.get('5', 0), tmp.get('6', 0), tmp.get('7+', 0), ]) / n_sum
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
                        print('<p>' + result[i][9] + text + u'''总进球数为%s的概率高达%.2f%%.''' % (count_text, rate * 100)) + '</p>'
                        break
                    count_text += '/'
    return content


# text = u'  按照爱竞彩的初盘统计系统，在相似竞彩奖金的情况下，本场比赛'
text = u'  爱竞彩初盘统计'
conn = MySQLdb.connect('localhost', 'root', '', 'oddsfair', charset="utf8")
cursor = conn.cursor()
cursor.execute("SELECT * FROM sporttery_baseinfo WHERE (date = Date(now()) AND time>Time(now())) "
               "OR date > Date(now()) ORDER BY data_id")
result = cursor.fetchall()
for i in xrange(len(result)):
    content = ''
    content = had_simulation(content)
    content = hhad_simulation(content)
    content = hafu_simulation(content)
    content = ttg_simulation(content)
    cursor.execute("SELECT * FROM tidian WHERE data_id = %s", result[i][1])
    tmp = cursor.fetchone()
    if not tmp and content != '':
        cursor.execute(
            "INSERT INTO tidian (data_id,num,date,tidianType10,content10,Team10,createUser,tidianStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (result[i][1], result[i][9], result[i][4], '3', content, '1', '3', '4'))
        conn.commit()
conn.close()
