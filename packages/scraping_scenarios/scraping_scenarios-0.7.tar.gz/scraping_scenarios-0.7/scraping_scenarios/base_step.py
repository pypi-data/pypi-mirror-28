from scraping_scenarios.logger import error


class BaseStep:

    # TODO: add unique identifiers for the step, so we could potentially track each step's status.

    def __init__(self, urls: list, some_name: str):

        """
        Basic idea of this class is to have a certain unit (step) that would do only one scraping related action.
        The goal might be a getting urls from the page or extracting certain information. It would be included in
        the scenarios, which can be implemented as an another class that would define the behaviour the crawler using
        the steps.

        Note to myself:
        This base class should be very general, because it potentially would be inherited to many other more specific
        and various kinds of steps.

        :param urls:
        """
        self.urls = urls
        self.some_name = some_name
        self.tree = None

    def execute_step(self, proxies: dict = None):
        """
        Depending on the purpose of this step, it will try to accomplish it, returning some object as a result.
        :return:
        """
        urls_list = []
        for url in self.urls:
            urls_list += self.step_action(url, proxies)
        if not urls_list:
            error('%s has been executed returning zero results.' % self.some_name)
        return urls_list

    def step_action(self, url, proxies: dict = None):
        """
        This step would potentially be inherited for the specific use.
        :param proxies:
        :param url:
        :return:
        """
        pass

    def get_single_attribute(self, xpath):
        attr = self.tree.xpath(xpath)
        if len(attr):
            return attr[0]
        else:
            return None

    def get_single_element(self, xpath):
        el = self.tree.xpath(xpath)
        if len(el):
            return el[0].text_content().strip()
        else:
            return None

    def set_urls(self, urls: list):
        """
        The method is aimed to be used when the step object would be used again, but with another url.
        :param urls:
        :return:
        """
        self.urls = urls

