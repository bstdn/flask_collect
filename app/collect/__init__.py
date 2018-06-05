class Collect_liaoxuefeng(object):
    from .spider_liaoxuefeng import spider_liaoxuefeng
    base_url = 'https://www.liaoxuefeng.com'
    spi = spider_liaoxuefeng()


collect = {
    'liaoxuefeng': Collect_liaoxuefeng
}


def create_collect(config_name):
    return collect[config_name]
