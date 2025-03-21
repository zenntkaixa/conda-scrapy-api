import json

import scrapy

"""
Scrapy spider to scrape quotes from the Quotes to Scrape API.
"""
class QuotesSpider(scrapy.Spider):
    name = "quotes" # Name of the spider
    allowed_domains = ["quotes.toscrape.com"] # Restrict crawling to this domain
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"] # Starting URL

    """
    Parse the JSON response and extract quote details.
    Args:
        response (scrapy.http.Response): The response object.
    """
    def parse(self, response):
        # Parse the JSON response into a Python dictionary
        json_response = json.loads(response.body)
        quotes = json_response.get('quotes') # Extract the list of quotes

        # Loop through each quote and extract details
        for quote in quotes:
            yield {
                'author': quote.get('author').get('name'),
                'tags': quote.get('tags'),
                'quotes': quote.get('text')
            }

        # Check if there is a next page
        has_next = json_response.get('has_next')
        if has_next:
            next_page_number = json_response.get('page') + 1

            # Log the next page number for debugging
            self.logger.info(f"Scraping page {next_page_number}...")

            # Request the next page
            yield scrapy.Request(
                url = f'https://quotes.toscrape.com/api/quotes?page={next_page_number}',
                callback = self.parse # Use the same parse method to handle the next page
            )