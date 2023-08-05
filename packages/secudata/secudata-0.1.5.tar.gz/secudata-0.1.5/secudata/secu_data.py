# coding=utf-8
import pandas as pd
import urllib2
import json
import time
import re

cookie = "s=8b17l424x8; webp=0; Hm_lvt_1db88642e346389874251b5a1eded6e3=1514512848,1514547571,1515392630,1515415006; __utma=1.1064058573.1488964716.1515392650.1515415015.85; __utmz=1.1514267849.81.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; device_id=540fc166a2dfe5e99adcd614651eb6aa; bid=4c4914f85f537cf909280dc3798e465b_j9hu2rrb; isPast=true; isPast.sig=Q1zWad3glPfOy3Ye-506BMax-a0; aliyungf_tc=AQAAABmbwlvQZQ4AT62QPcZyJBCee0Xj; xq_a_token=93ef7d84fd99d7b5f81ea4e1442c7252dff29d20; xq_a_token.sig=2_cWCFNwc-q7CurYUzOoewHw_DM; xq_r_token=18ddc4996d6018b400ebaaaa74f144296c288826; xq_r_token.sig=7749cnGDm8cToOaVZtCC3FKmJys; u=631515392629500; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1515415148; __utmc=1; __utmb=1.2.10.1515415015"
headers = {
		'Host': "xueqiu.com",
		'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
		'Accept': "*/*",
		'Cookie': cookie,
		'Connection': "close",
		'Upgrade-Insecure-Requests': "1",
		'Cache-Control': "max-age=0"
		}

K_TYPE = {
			'D':'1day',
			'W':'1week',
			'M':'1month',
			'1':'1m',
			'5':'5m',
			'15':'15m',
			'30':'30m',
			'60':'60m'
		}
def date_to(date_s):
    '''
    将’简化星期 简化月份 天数 小时(24):分钟:秒 时区 年份(四位数)’ 转化为 ’Y-m-d’
    Parameter
    ------
        date_s:string
                日期字符串， format: '%a %b %d %H:%M:%S %z %Y' e.g. 'Fri Dec 23 00:00:00 +0800 2016'
    return
    ------
        string
            日期字符串，format: '%Y-%m-%d %H:%M%S' e.g. '2017-12-04 00:00:00'
    注解：python2.7 版本下无法直接处理时区
    '''
    tmp = date_s.split(' ')
    del tmp[4]
    date_s = ' '.join(tmp)
    return time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(date_s,'%a %b %d %H:%M:%S %Y'))



def getData(symbol=None, start=None, end=None,
        ktype='D', autype='normal', retry_count=3, pause=0.05):
	'''
	获取股票当日交易记录
	Parameters
	-------
	 symbol: string
				股票标识 e.g. SH600000
	 start: string
				开始日期 format：YYYY-MM-DD 为空时默认为API最早日期, 分钟数据中没有作用
	 end: string		
				结束日期 format：YYYY-MM-DD 为空时去最近一个交易日，分钟数据中没有作用
         ktype：string
                数据类型，D=日k线 W=周 M=月 1=1分钟 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
         autype:string
                  复权类型，before-前复权 after-后复权 normal-不复权，默认为normal
	 retry_count: int, 默认 3
				如果遇到网络等问题重复执行的次数
	 pause: int, 默认 0.05
				重复请求数据过程中暂停的秒数, 防止请求间隔太短出现问题
	return
	-------
	 DataFrame
          属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，30日均价，换手率，成交额
          索引:日期
	'''
        pattern = r'^S[HZ][0-9]{6}$'
	if symbol is None:
            print "证券标识为空"
	    return pd.DataFrame()
        if re.match(pattern,symbol) == None:
            print "证券标识格式错误,'SH'/'SZ' + 证券代码(6位)"
            return pd.DataFrame()

	#start = '' if start is None else str(long(time.mktime(time.strptime(start,'%Y-%m-%d')) * 1000))
	#end = '' if end is None else str(long(time.mktime(time.strptime(end,'%Y-%m-%d')) * 1000))
	if ktype in ('1','5','15','30','60'):
		autype = 'normal'
	#link = 'https://xueqiu.com/stock/forchartk/stocklist.json?symbol='+ symbol+'&period='+K_TYPE[ktype.upper()]+'&type='+ autype +'&begin='+ start +'&end=' + end
	link = 'https://xueqiu.com/stock/forchartk/stocklist.json?symbol='+ symbol+'&period='+K_TYPE[ktype.upper()]+'&type='+ autype

	for _ in range(retry_count):
	    time.sleep(pause)
	    try:
                req = urllib2.Request(link, None, headers)
                response = urllib2.urlopen(req)
                content = response.read()
	    except Exception as e:
                print e
	    else:
                result = json.loads(content)
                if len(result) == 0:
                    return pd.DataFrame()
                data = result['chartlist']
                if len(data) == 0:
                    return pd.DataFrame()
                df = pd.read_json(json.dumps(data), dtype=False, convert_dates=False)
                df.drop(['macd','dif','dea','timestamp'],axis=1,inplace=True)
                df['timestamp'] = df['time'].map(date_to)
                if ktype in ('1', '5', '15', '30', '60'):
                    return df
                df['timestamp'] = df['timestamp'].map(lambda x: x[:10])
                df.set_index(['timestamp'],drop=False,inplace=True)
                return df[start:end]
	print "网络错误"
        return pd.DataFrame()
if __name__ == '__main__':
    print getData('SZ000002',start='2017-12-10',end='2017-12-18',autype='after')
	


