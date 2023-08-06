from scraping_scenarios.base_step import BaseStep
from scraping_scenarios.logger import info

from scraping_scenarios import utils


class URLCollectorStep(BaseStep):

    def __init__(self, urls: list, some_name: str, website_url: str, url_xpath: str = None):
        # TODO: inherit the exception to the specific one.
        super().__init__(urls, some_name)
        self.url_xpath = url_xpath
        self.website_url = website_url
        self.tree = None
        info('%s (URLCollectorStep) has been initialized.' % self.some_name)

    def step_action(self, url: str, send_result, proxies: dict = None):
        self.tree = utils.make_tree(url, proxies)
        if self.tree:
            result = utils.get_urls_from_tree(self.website_url, self.tree, self.url_xpath)
            return result
        else:
            return []


class SingleExtractingByXpathStep(BaseStep):

    def __init__(self, urls: list, some_name: str, xpaths: dict):
        super().__init__(urls, some_name)
        self.xpaths = xpaths
        self.tree = None
        info('%s (ExtractingByXpathStep) has been initialized.' % self.some_name)

    def step_action(self, url: str, send_result, proxies: dict = None):
        self.tree = utils.make_tree(url, proxies)
        if len(self.tree):
            result = utils.basic_parse_from_tree(self.tree, xpaths=self.xpaths)
            return [result]
        else:
            return [None]


class MultipleExtractByXpathStep(BaseStep):

    def __init__(self, urls: list, some_name: str, subtree_xpath: str, xpaths: dict, next_page_xpath: str = None):
        super().__init__(urls, some_name)
        self.xpaths = xpaths
        self.tree = None
        self.subtree_xpath = subtree_xpath
        self.next_page_xpath = next_page_xpath
        info('%s (ExtractingByXpathStep) has been initialized.' % self.some_name)

    def step_action(self, url: str, send_result, proxies: dict = None):
        self.tree = utils.make_tree(url, proxies)
        if self.tree:
            results = []
            if self.subtree_xpath:
                subtrees = self.tree.xpath(self.subtree_xpath)
                for subtree in subtrees:
                    scraped_data = utils.basic_parse_from_tree(subtree, xpaths=self.xpaths)
                    scraped_data['url'] = url
                    send_result(scraped_data)
                    results.append(scraped_data)
                return results
            else:
                results = utils.basic_parse_from_tree(self.tree, xpaths=self.xpaths)
                return results
        else:
            return [None]



"""plan:
    начинай читать код который ты написал связанный со следующей страницей.
    



"""
