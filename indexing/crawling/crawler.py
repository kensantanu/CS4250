# -------------------------------------------------------------------------
# FILENAME: crawler.py
# SPECIFICATION: Crawl the CPP Biology Dept Web until 10 Faculty Professors' pages with the required format are found.
#                The seed URL for the frontier is https://www.cpp.edu/sci/biological-sciences/index.shtml.
#                From the seed page, search through 10 professors' pages are found. Links might appear with
#                full or relative addresses, and the crawler needs to consider this.
#                Stop criteria: when the crawler finds 10 professors' pages with there required format.
#                For each traversed page, persist the page's URL along with HTML content in MongoDB collection.
# FOR: CS 4250- Group Project
# TIME SPENT: 4 hours
# -----------------------------------------------------------*/

# importing some Python libraries
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import regex as re
from database.db_connection import *


# Create a Frontier class to simulate a queue for the crawler to work on
class Frontier:
    """ Simulate a Queue class """
    def __init__(self):
        self.urls = []

    def is_empty(self):
        return len(self.urls) == 0

    def add_url(self, url):
        self.urls.append(url)

    def next_url(self):
        if not self.is_empty():
            return self.urls.pop(0)
        else:
            raise IndexError("Queue is empty")

    def size(self):
        return len(self.urls)

    def done(self):
        return not bool(self.urls)

    def clear_frontier(self):
        self.urls = []


def retrieve_url(url):
    """ Get the HTML content of the URL """
    try:
        html = urlopen(url)
        # CPP websites are originally encoded in binary form
        return html.read().decode(encoding="iso-8859-1")
    except HTTPError as e:
        return None
    except URLError as e:
        return None


def store_page(url, html, counter):
    """ Stores the page as a document in MongoDB database"""
    if html:
        # Connect to the database
        db = connectDataBase()
        # Create a collection to save the pages
        pages = db.pages
        # Save the URL and HTML content
        page = {'_id': counter, 'url': url, 'html': html}
        pages.insert_one(page)


def target_page(html):
    """ Detect if the crawler reaches the target page"""
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find_all('em', string=re.compile('.*Biological Sciences.*, College of Science'))


def parse(html):
    """ Traverse through the HTML content to discover all available URLs of other pages"""
    bs = BeautifulSoup(html, 'html.parser')
    # Extract all links from the page
    links = bs.find_all('a', href=True)
    return [link['href'] for link in links]


def crawler_thread(frontier):
    """ The Crawler to crawl the URLs and HTML contents"""
    targets_found = 0
    num_targets = 10
    target_urls = []  # To store the urls of the target pages
    crawled_pages = []  # List of crawled pages to check for duplicate before adding to the frontier
    counter = 0  # id of the page when adding to the MongoDB collection
    while not frontier.done():
        counter += 1
        url = frontier.next_url()
        crawled_pages.append(url)
        html = retrieve_url(url)
        store_page(url, html, counter)

        if html:  # Check if the html is not None
            if target_page(html):
                print(f"1 target page found: {url}")
                targets_found += 1
                target_urls.append(url)
            if targets_found == num_targets:
                frontier.clear_frontier()  # Clear the frontier
            else:
                for new_url in parse(html):
                    new_url = new_url.replace(' ', '')
                    is_abs_link = re.search('^http', new_url)
                    if is_abs_link:
                        full_url = new_url
                    else:
                        # urljoin will help join paths and handle relative path
                        full_url = urljoin(url, new_url)

                    # Check for duplicates before adding to the frontier
                    if full_url not in frontier.urls and full_url not in crawled_pages:
                        frontier.add_url(full_url)

    return target_urls
