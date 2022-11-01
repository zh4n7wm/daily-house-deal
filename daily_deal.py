#!/usr/bin/env python
# encoding: utf-8
"""
1. install python package
$ pip install requests lxml pandas

2. setup crontab (OS using `Asia/Shanghai`)
50 23 * * * cd /data/web/daily-house-deal && /home/wm/.virtualenvs/py3/bin/python daily_deal.py
"""
import logging
from datetime import date, datetime
from logging import handlers
from pathlib import Path

import pandas as pd
import requests
from lxml import html

LOG_FILENAME = '/tmp/logs/house/daily_deal.log'
p = Path(LOG_FILENAME)
if not p.parent.exists():
    p.parent.mkdir(parents=True)
del p
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler = handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1 * 1024 * 10,
    backupCount=5,
)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def get_daily_deal():
    url = 'https://zw.cdzjryb.com/SCXX/Default.aspx?action=ucEveryday2'
    headers = {
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    req = requests.get(url, headers=headers)
    charset = req.encoding or 'utf-8'
    tree = html.fromstring(req.content.decode(charset))
    td_count = 5
    tmp = [x.strip() for x in tree.xpath('//tr[@bgcolor="#FFFFFF"]/td/text()')]
    data = list(zip(*(iter(tmp),) * td_count))
    res = []
    if len(data) != 6:
        logger.warning('Something wrong, you need check web page.')
    else:
        for i, x in enumerate(data):
            house_type = '新盘' if i < 3 else '二手房'
            res.append({
                'date': datetime.now().isoformat(),
                'house_type': house_type,
                'district': x[0],
                'total_area': float(x[1]),
                'number': int(x[2]),
                'residential_area': float(x[3]),  # 商品住宅面积 或者 二手住宅面积
                'non_residential_area': float(x[4]),  # 商品住宅面积 或者 二手住宅面积
            })

    return res


if __name__ == '__main__':
    logger.debug('get house deal information.')
    res = get_daily_deal()
    header = [
        'date', 'district', 'house_type', 'total_area', 'number',
        'residential_area', 'non_residential_area'
    ]
    new_df = pd.DataFrame(res)
    new_df = new_df[header]
    csv_path = './daily-house-deal.csv'
    df = pd.read_csv(csv_path)
    today = date.today()
    if pd.to_datetime(df.date).dt.date.iloc[-1] == today:
        logger.debug('remove today old data...')
        delete_lst = df[pd.to_datetime(df.date).dt.date == today].index
        df.drop(delete_lst, inplace=True)
    df = df.append(new_df)
    with open(csv_path, 'w') as fd:
        logger.debug('save to csv file.')
        df.to_csv(fd, index=False, header=True)
    logger.debug('done.')
    # print(json.dumps(res, indent=4, ensure_ascii=False))
