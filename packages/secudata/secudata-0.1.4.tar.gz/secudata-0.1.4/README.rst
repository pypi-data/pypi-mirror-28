========================
secudata 0.1.4
========================
A Python library for getting *security data* of *China*.

------------------------
Installation
------------------------
- *pip install secudata*

------------------------
Function Introduction
------------------------
::

    def getData(symbol=None, start=None, end=None,ktype='D', autype='normal', retry_count=3, pause=0.05):
    获取股票当日交易记录
    Parameters:
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
    Return:
        DataFrame:
                属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，30日均价，换手率，成交额
                索引:日期

------------------------
Quick Start
------------------------
::

    import secudata as sd
    sd.getData('SH000001')

::

    return:
        DataFrame:
        属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，30日均价，换手率，成交额
          
        索引:日期

-------------------------
Require_package
-------------------------
- pandas
