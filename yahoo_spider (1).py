# to run 
# scrapy crawl yahoo_spider -o results.csv

import scrapy
from urllib.parse import urljoin

class yahooscraper(scrapy.Spider):
    name = 'yahoo_spider'

    start_urls = ["https://finance.yahoo.com/most-active?count=25&offset=0"
                 # "https://finance.yahoo.com/most-active?count=25&offset=25"
                 ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_quote)

    def parse_quote(self, response):
        link_elements = response.xpath('//a[@data-test="quoteLink"]')

        tickers = response.css('a[data-test="quoteLink"]::text').getall()
        company_names = response.css('a[data-test="quoteLink"]::attr(title)').getall()

        for ticker, company_name, link in zip(tickers, company_names, link_elements):
            # Extract the 'href' attribute value
            link_url = link.xpath('@href').get()
            url = urljoin('https://finance.yahoo.com', link_url)

            # Send a request to parse_history with meta information
            yield scrapy.Request(url=url, callback=self.parse_history, meta={'ticker': ticker.strip(), 'company_name': company_name.strip()})

    def parse_history(self, response):
        # Extract historical URL
        history_url = response.css('a[href^="/quote/"][href*="/history"]::attr(href)').get()
        url = urljoin('https://finance.yahoo.com', history_url)

        # Extract meta information
        ticker = response.meta.get('ticker', '')
        company_name = response.meta.get('company_name', '')

        # Yield the data to be written to the CSV file
        yield {
            "ticker": ticker,
            "company name": company_name,
            "hist_url": url
        }
    