import scrapy
import json
import os


class F1CommentarySpider(scrapy.Spider):
    name = "f1_commentaryspider"
    allowed_domains = ["motorsport.com"]
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,  # Be polite to the server
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        """Load initial requests from links.json."""
        file_path = "links.json"
        if not os.path.exists(file_path):
            self.logger.error(f"File {file_path} not found!")
            return

        try:
            with open(file_path, "r") as file:
                links = json.load(file)

            for link in links:
                race_id = link["link"].split("/")[-2]  # Extract the race ID
                initial_url = f"https://www.motorsport.com/live-text-messages/{race_id}/?p=1"
                yield scrapy.Request(
                    url=initial_url,
                    callback=self.parse_commentary,
                    meta={
                        "race_id": race_id,
                        "page": 1,
                        "original_link": link["link"]
                    },
                    errback=self.handle_error
                )
        except json.JSONDecodeError:
            self.logger.error("Failed to parse links.json file")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")

    def parse_commentary(self, response):
        """Parse commentary and handle pagination."""
        race_id = response.meta["race_id"]
        current_page = response.meta["page"]

        # Extract all commentary blocks from the page
        commentary_blocks = response.css('div.mslt-msg')

        if not commentary_blocks:
            self.logger.info(f"No more commentary on page {current_page} for race {race_id}.")
            return

        # Process each block
        for block in commentary_blocks:
            try:
                # Extract timestamp, message, and author
                timestamp = block.css('div.mslt-msg__time::text').get()
                message = ' '.join([
                    text.strip()
                    for text in block.css('div.mslt-msg__body ::text').getall()
                    if text.strip()
                ])
                author = block.css('div.mslt-msg__author::text').get()

                if message:  # Yield only if message exists
                    yield {
                        "race_id": race_id,
                        "page": current_page,
                        "timestamp": timestamp.strip() if timestamp else None,
                        "commentary": message,   
                    }
            except Exception as e:
                self.logger.error(f"Error processing commentary block: {str(e)}")

        # Check if there is a next page
        next_page = current_page + 1
        next_url = f"https://www.motorsport.com/live-text-messages/{race_id}/?p={next_page}"

        # Check if commentary still exists on the next page
        if len(commentary_blocks) > 0:
            self.logger.info(f"Fetching page {next_page} for race {race_id}.")
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_commentary,
                meta={
                    "race_id": race_id,
                    "page": next_page,
                    "original_link": response.meta["original_link"]
                },
                errback=self.handle_error
            )

    def handle_error(self, failure):
        """Handle request errors."""
        self.logger.error(f"Request failed: {failure.request.url}")
        meta = failure.request.meta
        self.logger.error(f"Failed while processing race_id: {meta.get('race_id')}, page: {meta.get('page')}")
