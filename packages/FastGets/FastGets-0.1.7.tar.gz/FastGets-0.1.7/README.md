# FastGets

>FastGets is a user-friendly web crawling framework. It is very suitable for individuals or enterprises to efficiently develop crawler code and extract structured data from websites.

**FastGets is designed according to the way of User Thinking. User do not need to know the complex underlying logic of framework, do not need to spend energy on configuration parameters, do not need to rack his brains to think of the usage of a function. User only needs to know which pages on which websites he wants to crawl and write down some simple code which has fixed routines according to the way of browsing the website.**

**FastGets is designed to help users to get the data of the websites by a quick and accurate way. The advantage of FastGets is who uses who knows.**

## Installation
FastGets works on Python3.

You can install it via pip
```bush
$ pip3 install git+git://github.com/ShuJuHeiKe/FastGets.git
```
or clone it and install it
```bush
$ git clone --recursive https://github.com/ShuJuHeiKe/FastGets.git
$ cd FastGets
$ pip3 install -r pip-req.txt
$ python3 setup.py install
```

## Basic Usage
huxiu.py
```python
# coding: utf8

import re
import json
import lxml.html
from fastgets import Task, TemplateBase, CsvWriter


writer = CsvWriter('article.csv', ['ID', '标题', '链接'])


class Huxiu(TemplateBase):

    """
    抓取虎嗅网新闻
    """

    config = {
        'second_rate_limit': 2,
    }

    @classmethod
    def load(cls):

        task = Task()
        task.url = 'https://www.huxiu.com/article/229671.html'
        task.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        task.timeout = 10
        task.func = cls.parse_article_detail_page
        task.add()

    @classmethod
    def parse_article_detail_page(cls, task, page_raw):

        doc = lxml.html.fromstring(page_raw)
        id = doc.xpath('//div[@class="article-section"]/@data-aid')[0]
        title = doc.xpath('//h1[@class="t-h1"]/text()')[0].strip()

        writer.add((id, title, task.url))

if __name__ == '__main__':
    Huxiu.run()
```


## Introduction & Examples
Spider，like huxiu.py， has 3 mode to run.

* test mode

The way to run the spider when you write the code.

```bush
$ python3 huxiu.py -m t
```

* local mode

Run the spider and get a small amount of data from websites after you finsh the spider code.

```bush
$ python3 huxiu.py -m l
```
 **How to write the spider code? How to use the test mode and local mode to run the spider? You just need to Click the link below.  https://github.com/ShuJuHeiKe/MySimpleProject**

* distributed mode

This mode is suitable for getting large amounts of data.
```bush
$ python3 huxiu.py -m d
```
**Before you run, you need install `redis` and `mongodb`, and start them. After those, you will find you can not sucess to crawl the page of the website.**

**If you want to know how to `easily` build the distributed cluster and start them, you just need to click the link below.
  https://github.com/ShuJuHeiKe/MyProject**
