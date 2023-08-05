import os
import csv
from urllib.parse import urlparse
from stylelens_crawl import PKG_DIR
from urllib.parse import quote_plus


def make_url_encode_in_path(url):
    words = url.split(sep='/')
    words = [quote_plus(word) for word in words]
    return '/'.join(words)


# TODO: 함수 최적화가 필요해보임, 다만 현재는 복잡하지만 이렇게 나눔
def make_url(domain, location):
    url = urlparse(location)
    domain = urlparse(domain)
    if url.scheme == '' and url.netloc == '':
        if len(url.query):
            return 'http://' + domain.netloc + make_url_encode_in_path(url.path) + '?' + url.query
        else:
            return 'http://' + domain.netloc + make_url_encode_in_path(url.path)
    elif url.scheme == '':
        if len(url.query):
            return 'http://' + url.netloc + make_url_encode_in_path(url.path) + '?' + url.query
        else:
            return 'http://' + url.netloc + make_url_encode_in_path(url.path)
    else:
        return url.geturl()


def get_netloc(domain):
    url = urlparse(domain)
    return url.scheme, url.netloc, url.path


def get_shopping_information_from_csv(host_code):
    with open(os.path.join(PKG_DIR, 'stylelens_crawl/data/sites/site.csv'), 'r', encoding='utf-8') as file:
        data = csv.reader(file)
        for item in data:
            if item[0] == host_code:
                return item
