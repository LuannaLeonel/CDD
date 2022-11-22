import scrapy

from .utils.DataScrapy import DataScrapy


class QuotesSpider(scrapy.Spider):
    name = "deputadas"

    def start_requests(self):

        deps_file = open("../entries/deputadas.txt", "r")

        deps_urls = deps_file.read().splitlines()

        for url in deps_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data_getter = DataScrapy(response)

        dep_data = data_getter.run(gender="F")

        yield dep_data

