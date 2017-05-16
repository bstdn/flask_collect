import requests
import re


class spider_liaoxuefeng(object):
    def get_source(self, url):
        ret = ''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        if r.status_code == 200:
            ret = r.text
        return ret

    def get_title(self, html):
        return re.search('(?<=<title>).*?(?=</title>)', html, re.S).group()

    def get_body(self, html):
        return re.search('(?<=<div class="x-wiki-content">).*?(?=</div>)', html, re.S).group()

    def get_page_list(self, html):
        url_box = re.search('(?<=<ul class="uk-nav uk-nav-side" style="margin-right:-15px;">).*?(?=</ul>)',
                            html, re.S).group()
        url_list = re.findall('href="(.*?)">(.*?)</a>', url_box, re.S)
        new_url_list = [(url, name) for url, name in url_list]
        return new_url_list

    def get_index_list(self, html):
        category = [r'JavaScript教程', r'Python教程', r'Git教程']
        url_box = re.search('(?<=<ul id="ul-navbar" class="uk-navbar-nav uk-hidden-small">).*?(?=</ul>)',
                            html, re.S).group()
        url_list = re.findall('href="(.*?)">(.*?)</a>', url_box, re.S)
        new_url_list = []
        for url, name in url_list:
            if name in category:
                new_url_list.append((url, name))
        return new_url_list
