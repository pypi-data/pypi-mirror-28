from base_step import BaseStep
from logger import info

from scraping_scenarios import utils


class URLCollectorStep(BaseStep):

    def __init__(self, urls: list, some_name: str, website_url: str, url_xpath: str = None):
        # TODO: inherit the exception to the specific one.
        super().__init__(urls, some_name)
        self.url_xpath = url_xpath
        self.website_url = website_url
        info('%s (URLCollectorStep) has been initialized.' % self.some_name)

    def step_action(self, url: str):
        tree = utils.make_tree(url)
        if tree:
            result = utils.get_urls_from_tree(self.website_url, self.url_xpath)
            return result
        else:
            return []


class ExtractingByXpathStep(BaseStep):

    def __init__(self, urls: list, some_name: str, xpaths: dict):
        super().__init__(urls, some_name)
        self.xpaths = xpaths
        info('%s (ExtractingByXpathStep) has been initialized.' % self.some_name)

    def step_action(self, url: str):
        tree = utils.make_tree(url)
        if tree:
            result = utils.basic_parse_from_tree(tree, xpaths=self.xpaths)
            return [result]
        else:
            return [None]
