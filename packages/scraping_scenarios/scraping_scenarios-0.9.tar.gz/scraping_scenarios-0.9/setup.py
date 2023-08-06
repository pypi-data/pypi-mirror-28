from distutils.core import setup
setup(
  name = 'scraping_scenarios',
  packages = ['scraping_scenarios'],
  version = '0.9',
  description = 'A framework containing basic scenarios and steps for web crawling. Aim is to simplify the coding '
                'of web crawlers/workers',
  author = 'Ulugbek Babazhanov',
  author_email = 'ulugbek.babazhanov@nu.edu.kz',
  url = 'https://github.com/Dracula999/scraping_scenarios',
  download_url = 'https://github.com/Dracula999/scraping_scenarios/archive/v0.1.tar.gz',
  keywords = ['testing', 'logging', 'example'],
  install_requires = ['requests', 'lxml', 'dateparser'],
  classifiers = [],
)
