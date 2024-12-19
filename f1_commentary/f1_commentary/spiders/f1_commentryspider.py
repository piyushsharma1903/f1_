import scrapy

class f1commentaryspider(scrapy.Spider):
    name = "f1_commentaryspider"
    allowed_domains = ["motorsport.com"]
    start_urls = ["https://www.motorsport.com/live/?p=13"]

    def parse(self, response):
        # Extract links
        anchor_tags = response.css('div.ms-grid a.ms-item::attr(href)').getall()
        for link in anchor_tags:
            full_url = response.urljoin(link)
            yield {"link": full_url}