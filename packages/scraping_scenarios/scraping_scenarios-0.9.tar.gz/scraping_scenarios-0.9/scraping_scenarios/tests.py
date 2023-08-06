from scraping_scenarios.scenarios import SearchWebsiteScenario, ForumsScenario
from scraping_scenarios.logger import info
from scraping_scenarios.scraping_steps import MultipleExtractByXpathStep, URLCollectorStep


def prepare_post(url: str, text: str, date: str, owner_id: str, owner_name: str):
    post = {
        'comment_count': 0,
        'date': convert_datetime(date),
        'discriminator': DISCRIMINATOR_POST,
        'id': get_id_from_content(text),
        'like_count': 0,
        'owner_id': owner_id,
        'owner_name': owner_name,
        'owner_type': OWNER_TYPE,
        'platform_id': PLATFORM_ID,
        'repost_count': 0,
        'search_field': SEARCH_FIELD,
        'text': text.strip() + '\n#forums_test',
        'url': url
    }
    return post


def get_next_page_url(tree):
    next_page_xpath = './/li[@class="next"]/a/@href'
    next_page_url = tree.xpath(next_page_xpath)
    if len(next_page_url):
        return next_page_url[0]
    else:
        return None


def send_result(scraped_data: dict):
    info(str(scraped_data['post_date']) + ' - ' + scraped_data['post_text'].strip())


def test_kris_forum():
    MAIN_WEBSITE = 'http://forum.kris.kz/'
    # xpaths
    FORUMS_URLS = './/table[@class="table_list"]/tbody/tr[@class="windowbg2"]/td[@class="info"]/a[@class="subject"]/@href'
    TOPICS_URLS = './/td[contains(@class, "subject")]//span[contains(@id, "msg")]/a/@href'
    ALL_PAGES = './/div[contains(@class, "pagelinks")]/a[@class="navPages"]'
    CERTAIN_PAGE = './/div[contains(@class, "pagelinks")]/a[@class="navPages" and text()=%s]/@href'

    # xpaths
    FORUMS_LIST_URLS = './/tr/td[@class="col_c_forum"]/h4/a/@href'
    THREAD_LIST_URLS = './/td/h4/a[@class="topic_title"]/@href'
    NEXT_PAGE = './/div[contains(@class, "topic_controls")]//li[@class="next"]/a/@href'

    POSTS_XPATH = './/div[@id="forumposts"]//div[contains(@class, "window")]'
    POST_DATE_XPATH = './/div[@class="smalltext"]'
    POST_TEXT_XPATH = './/div[@class="post"]/div[@class="inner"]'
    AUTHOR_URL_XPATH = './/div[@class="poster"]//a/@href'
    AUTHOR_NAME_XPATH = './/div[@class="poster"]//a'
    POSTER_PIC_URL = 'http://forum.detki.kz/public/style_images/master/profile/default_large.png'
    xpaths = {'post_text': POST_TEXT_XPATH, 'post_date': POST_DATE_XPATH, 'post_author_name': AUTHOR_NAME_XPATH,
              'post_author_url': AUTHOR_URL_XPATH}
    forums_scenario = ForumsScenario(MAIN_WEBSITE, FORUMS_URLS, TOPICS_URLS, POSTS_XPATH, xpaths)
    forums_scenario.execute_scenario(get_next_page=None, send_result=send_result)


def test_karapuz_forum():
    MAIN_WEBSITE = 'http://forum.karapuz.kz/'

    # xpaths
    FORUMS_LIST_URLS = './/tr/td[@class="col_c_forum"]/h4/a/@href'
    THREAD_LIST_URLS = './/td/h4/a[@class="topic_title"]/@href'
    NEXT_PAGE = './/div[contains(@class, "topic_controls")]//li[@class="next"]/a/@href'

    POSTS_XPATH = './/div[@class="ipsBox_container"]/div[contains(@id, "post_id")]'
    POST_DATE_XPATH = './/abbr[@itemprop="commentTime"]/@title'
    POST_TEXT_XPATH = './/div[@itemprop="commentText"]'
    LOGGED_AUTHOR_NAME_XPATH = './/span[contains(@class, "author") and contains(@class, "vcard")]'
    LOGGED_AUTHOR_URL_XPATH = 'http://forum.karapuz.kz/'
    LOGGED_AUTHOR_PIC_URL_XPATH = './/li[@class="avatar"]/img/@src'
    xpaths = {'post_text': POST_TEXT_XPATH, 'post_date': POST_DATE_XPATH, 'post_author_name': LOGGED_AUTHOR_NAME_XPATH}
    forums_scenario = ForumsScenario(MAIN_WEBSITE, FORUMS_LIST_URLS, THREAD_LIST_URLS, POSTS_XPATH, xpaths)
    forums_scenario.execute_scenario(get_next_page=None, send_result=send_result)


def test_keden_forum():
    # xpaths
    FORUMS_LIST_URLS = './/a[@class="forumtitle"]/@href'
    THREAD_LIST_URLS = './/a[@class="topictitle"]/@href'
    MAIN_WEBSITE = 'http://forum.keden.kz/'

    ALL_PAGES = './/div[@class="pagination"]/span/a'
    CERTAIN_PAGE = './/div[@class="pagination"]/span/a[text()=%s]/@href'

    POST_TITLE = './/div[@id="page-body"]/h2/a'
    POSTS_XPATH = './/div[@id="page-body"]/div[contains(@class, "post")]'
    AUTHOR_XPATH = './/p[@class="author"]'
    AUTHOR_URL_XPATH = './/strong/a/@href'

    AUTHOR_NAME_XPATH = './/strong/a'
    POST_DATE_XPATH = './/text()'

    POST_TEXT_XPATH = './/div[@class="content"]'
    xpaths = {'post_text': POST_TEXT_XPATH, 'post_date': POST_DATE_XPATH, 'post_author_name': AUTHOR_NAME_XPATH,
              'post_author_url': AUTHOR_URL_XPATH}
    forums_scenario = ForumsScenario(MAIN_WEBSITE, FORUMS_LIST_URLS, THREAD_LIST_URLS, POSTS_XPATH, xpaths)
    forums_scenario.execute_scenario(get_next_page=None, send_result=send_result)


def test_detki_forum():
    # xpaths
    FORUMS_LIST_URLS = './/tr/td[@class="col_c_forum"]/h4/a/@href'
    THREAD_LIST_URLS = './/td/h4/a[@class="topic_title"]/@href'
    NEXT_PAGE = './/div[contains(@class, "topic_controls")]//li[@class="next"]/a/@href'
    MAIN_WEBSITE = 'http://forum.detki.kz/'

    POSTS_XPATH = './/div[@class="ipsBox_container"]/table'
    POST_DATE_XPATH = './/abbr[@itemprop="commentTime"]/@title'
    POST_TEXT_XPATH = './/div[@itemprop="commentText"]'
    LOGGED_AUTHOR_NAME_XPATH = './/a[@hovercard-ref="member"]/span'
    LOGGED_AUTHOR_URL_XPATH = './/a[@hovercard-ref="member"]/@href'
    LOGGED_AUTHOR_PIC_URL_XPATH = './/li[@class="avatar"]/a/img/@src'

    xpaths = {'post_text': POST_TEXT_XPATH, 'post_date': POST_DATE_XPATH, 'post_author_name': LOGGED_AUTHOR_NAME_XPATH,
              'post_author_url': LOGGED_AUTHOR_URL_XPATH}
    forums_scenario = ForumsScenario(MAIN_WEBSITE, FORUMS_LIST_URLS, THREAD_LIST_URLS, POSTS_XPATH, xpaths)
    forums_scenario.execute_scenario(get_next_page=get_next_page_url, send_result=send_result)


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
    forums_scenario.execute_scenario(get_next_page=get_next_page_url, send_result=send_result)


def test_mamamia_forum():
    # xpaths
    website_url = 'http://mamamia.kz/index.php?sid=61ef79a80e682866a320772ffe1ed2bb'

    FORUMS_LIST_URLS = './/tr/td[@class="col_c_forum"]/h4/a/@href'
    THREAD_LIST_URLS = './/td/h4/a[@class="topic_title"]/@href'
    NEXT_PAGE = './/div[contains(@class, "topic_controls")]//li[@class="next"]/a/@href'

    POSTS_XPATH = './/div[@class="ipsBox_container"]/table'
    POST_DATE_XPATH = './/abbr[@itemprop="commentTime"]/@title'
    POST_TEXT_XPATH = './/div[@itemprop="commentText"]'
    LOGGED_AUTHOR_NAME_XPATH = './/a[@hovercard-ref="member"]/span'
    LOGGED_AUTHOR_URL_XPATH = './/a[@hovercard-ref="member"]/@href'
    LOGGED_AUTHOR_PIC_URL_XPATH = './/li[@class="avatar"]/a/img/@src'


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
