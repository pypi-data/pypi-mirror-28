from scraping_scenarios.scenarios import SearchWebsiteScenario
from scraping_scenarios.logger import info


if __name__ == '__main__':
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

