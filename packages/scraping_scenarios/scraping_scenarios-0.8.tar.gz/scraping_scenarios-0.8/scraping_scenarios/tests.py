from scraping_scenarios.scenarios import SearchWebsiteScenario, ForumsScenario
from scraping_scenarios.logger import info
from scraping_scenarios.scraping_steps import MultipleExtractByXpathStep, URLCollectorStep


def test_dieslcat_forum():
    website_url = 'http://diesel.elcat.kg/'
    forum_xpath = './/td[@class="col_c_forum"]/h4/a/@href'
    thread_xpath = './/h4/a[@class="topic_title"]/@href'
    post_xpath = './/div[@class="post_block hentry clear clearfix  "]'
    post_text_xpath = './/div[@class="post entry-content "]'
    post_date_xpath = './/*[@itemprop="commentTime"]'
    post_author_name_xpath = './/span[@class="author vcard"]//span[@itemprop="name"]'
    post_author_url_xpath = './/span[@class="author vcard"]/a/@href'

    xpaths = {'post_text': post_text_xpath, 'post_date': post_date_xpath, 'post_author_name': post_author_name_xpath,
              'post_author_url': post_author_url_xpath}

    forums_scenario = ForumsScenario(website_url, forum_xpath, thread_xpath, post_xpath, xpaths)
    forums_scenario.execute_scenario()


def test_search_scenarios():
    info('Testing for the bing.com: ')
    search_strings = ['hello']
    search_url_scheme = '%s?q=%s'

    duckduckgo_search = SearchWebsiteScenario('https://duckduckgo.com/', search_strings, search_url_scheme,
                                              './/h2[@class="result__title"]/a/@href',
                                              './/input[@value="Next"]/')
    results = duckduckgo_search.execute_scenario()
    for search_string in search_strings:
        info(results[search_string])
    bing_search = SearchWebsiteScenario('https://bing.com/', search_strings, '%ssearch?q=%s',
                                        './/ol[@id="b_results"]/li/h2/a/@href', './/a[@class="sb_pagN"]/@href', 3)
    results = bing_search.execute_scenario()
    for search_string in search_strings:
        info(results[search_string])

    info('Testing for the yandex.ru')
    yandex_search = SearchWebsiteScenario('https://yandex.kz/', search_strings, '%ssearch/?text=%s',
                                          './/li[contains(@class, "serp-item")]/div/h2/a/@href',
                                          './/a[contains(@class, "pager__item_kind_next")]/@href', 3)
    results = yandex_search.execute_scenario()
    for search_string in search_strings:
        info(results[search_string])

