"""
This Scrapy project follows the YouTube tutorial video: "Scrapy Course – Python Web Scraping for Beginners "
Link: https://www.youtube.com/watch?v=mBoX_JCKZTE
Course created by Joe Kearney.
"""

import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # look for all articles of class "product_pod" and store as list of books
        books = response.css("article.product_pod")

        # loop through each book element and return attributes as dictionary
        for book in books:
            yield {
                "name": book.css("h3 a ::text").get(),
                "price": book.css(".product_price .price_color ::text").get(),
                "url": book.css("h3 a").attrib["href"]
            }

        # find and store href from next page button
        next_page = response.css("li.next a ::attr(href)").get()

        # if "catalogue/" is in next page href (ie. first page)
        if "catalogue/" in next_page:

            # create full URL address with base url and href
            next_page_url = f"{self.start_urls[0]}{next_page}"

            # go to next page address and repeat parse function
            yield response.follow(next_page_url, callback=self.parse)

        # if "catalogue/" is not in next page href, add to url
        else:
            next_page_url = f"{self.start_urls[0]}catalogue/{next_page}"
            yield response.follow(next_page_url, callback=self.parse)
