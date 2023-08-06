from scraping_scenarios.scraping_steps import URLCollectorStep, MultipleExtractByXpathStep
from scraping_scenarios.base_scenario import BaseScenario
from scraping_scenarios.logger import info
from scraping_scenarios import utils


class SearchWebsiteScenario(BaseScenario):

    def __init__(self, website_url: str, search_strings: list, search_url_schema: str,
                 url_xpath: str, next_page_xpath: str = None, page_limit: int = 0):
        """
            This scraping scenario is for the search websites. It will collect search results.
            Three steps: 1) enter the search string, 2) collect results from the page 3) get the next page.
            For the first step we can just insert the search query in the url ( works for at least for
            bing, yandex, duckduckgo). Then, as we get the page, using the xpath for the result url, we collect them.
            Once we collected result urls, we move to the next page. To do that, we will need an xpath for the
            next page button. Specifically for button's @href attribute. As we get the url for the next page, we do the
            step 2 again, basically looping through steps 2 and 3 until there is not next page.
            There is also can be a limitation to the maximum number of result pages to scrape result urls from.
            page_limit by default is 0, which means that there is no page limit.
        """
        super().__init__()
        self.website_url = website_url
        self.page_limit = page_limit
        self.search_strings = search_strings
        self.search_url_schema = search_url_schema
        self.url_xpath = url_xpath
        self.next_page_xpath = next_page_xpath

    def execute_scenario(self, proxies: dict = None):
        all_results = {}
        for search_string in self.search_strings:
            page_counter = 0
            search_url = self.search_url_schema % (self.website_url, search_string)
            info(search_url)
            collect_results_step = URLCollectorStep([search_url], 'Search website', self.website_url, self.url_xpath)
            results = collect_results_step.execute_step(proxies=proxies)
            next_page = True
            if self.next_page_xpath:
                while next_page and (page_counter < self.page_limit or self.page_limit == 0):
                    next_page_url = collect_results_step.get_single_attribute(self.next_page_xpath)
                    if next_page_url:
                        next_page_url = utils.form_schemed_url(next_page_url, self.website_url)
                        info('Got the next page. ' + next_page_url)
                        collect_results_step.set_urls([next_page_url])
                        results += collect_results_step.execute_step(proxies=proxies)
                    else:
                        next_page = False
                    page_counter += 1
            all_results[search_string] = results
        return all_results


class ForumsScenario(BaseScenario):
    def __init__(self, website_url: str, forum_xpath: str, thread_xpath: str, post_xpath: str, post_info_xpaths: dict):
        super().__init__()
        self.website_url = website_url
        self.forum_xpath = forum_xpath
        self.thread_xpath = thread_xpath
        self.post_xpath = post_xpath
        self.post_info_xpaths = post_info_xpaths
        pass

    def execute_scenario(self, get_next_page=None, send_result=None):
        self.collect_forums(self.website_url, get_next_page, send_result)
        pass

    def collect_forums(self, url, get_next_page, send_result):
        collect_forums_urls_step = URLCollectorStep([url], 'Forums collector', self.website_url, self.forum_xpath)
        forum_urls = collect_forums_urls_step.execute_step(get_next_page=None, send_result=None)
        for forum_url in forum_urls:
            self.collect_forums(forum_url, get_next_page, send_result)
        collect_threads_urls_step = URLCollectorStep([url], 'Threads collector', self.website_url, self.thread_xpath)
        thread_urls = collect_threads_urls_step.execute_step(get_next_page, send_result=None)
        info('Found ' + str(len(thread_urls)) + ' threads')
        collect_posts_step = MultipleExtractByXpathStep(thread_urls, 'Post collector', self.post_xpath, self.post_info_xpaths)
        collect_posts_step.execute_step(get_next_page, send_result)

    def deal_with_results(self, res: list):
        pass
