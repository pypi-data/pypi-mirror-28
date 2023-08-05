import traceback

import lxml.html as html
import requests

from logger import error, info, warning

default_headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0",
    'Accept-Language': "en-US,en;q=0.5",
    'Content-Type': 'application/json; charset=utf-8'
}


def form_schemed_url(url: str, domain: str):
    if url.startswith('http'):
        return url
    else:
        if url.startswith('/'):
            if not domain.endswith('/'):
                return domain + url
            else:
                return domain[:-1] + url
        else:
            if not domain.endswith('/'):
                return domain + '/' + url
            else:
                return domain + url


def get_urls_from_tree(domain: str, tree, url_xpath: str = None):
    """
    Using the beautiful lxml.html module we can easily extract all available links which are enclosed by 'a' tagname.
    Receiving html tree block we take all urls. Also, considered cases, when the attribute @href doesn't contain
    the hostname before the url. We add the hostname and also check for the extra slashes.
    :param url_xpath:
    :param domain:
    :param tree:
    :return:
    """
    if url_xpath:
        urls = tree.xpath(url_xpath)
    else:
        urls = tree.xpath('.//a/@href')
    for index, url in enumerate(urls):
        urls[index] = form_schemed_url(url, domain)
    return urls


def basic_parse_from_tree(tree, xpaths: dict, xpaths_default: dict = None):
    results = {}
    for key in xpaths:
        xpath = xpaths[key]
        if xpath:
            temp = tree.xpath(xpath)
            if len(temp):
                str_element = temp[0].text_content().strip()
                results[key] = str_element
            else:
                results[key] = ' '
        else:
            results[key] = None
    return results


def basic_parse_from_url(url: str, xpaths: dict):
    result = {}
    tree = make_tree(url)
    if tree:
        for key in xpaths:
            xpath = xpaths[key]
            if xpath:
                temp = tree.xpath(xpath)
                if temp:
                    str_element = temp[0].text_content().strip()
                    result[key] = str_element
                else:
                    result[key] = None
            else:
                result[key] = None
        return result
    else:
        error('Could not form a tree from the url: %s' % url)
        return None


def make_tree(url: str):
    """
    make lxml.html tree from string. Checks included.
    :param url:
    :return:
    """
    response = get_response(url)
    if response:
        if response.ok:
            tree = html.fromstring(response.text)
            return tree
        else:
            error('Response status code is not 200: ' + str(response.status_code) + '\n url: ' + url)
            response.close()
            return None


def get_response(url: str, max_retries: int = 3, headers: dict = default_headers, proxies: dict = None):
    retries = 0
    while True:
        try:
            if proxies:
                response = requests.get(url, headers=headers, proxies=proxies)
            else:
                response = requests.get(url, headers=headers)
            return response
        except requests.Timeout:
            warning('Request time out.')
            if retries == max_retries:
                error('Reached maximum amount of retries. The problem described below:\n' + traceback.format_exc())
                break
            retries += 1
            info('Try number: ' + str(retries))
