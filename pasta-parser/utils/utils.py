# utils.py

import requests
from bs4 import BeautifulSoup
import logging


def fetch_html(url):
    """Fetch the HTML content of a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None


def parse_html(html):
    """Parse HTML content using BeautifulSoup."""
    return BeautifulSoup(html, 'html.parser')


def extract_text(soup):
    """Extract text from parsed HTML."""
    paragraphs = soup.find_all('article')
    return paragraphs.contents

def format_message(message, id):
    return {
        "_id": id,
        "text": message,
    }


def is_valid_url(url):
    """Basic URL validation."""
    return url.startswith("http")
