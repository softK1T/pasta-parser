# pasta_parser/utils/parser_utils.py

import logging
import re

import requests
from bs4 import BeautifulSoup


class PageParser:
    @staticmethod
    def fetch_page(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch page {url}: {str(e)}")
            return None

    @staticmethod
    def parse_body(raw_body):
        # Example method to clean up the body text, if needed
        return raw_body.replace('\n', ' ').replace('\r', '')

    @staticmethod
    def find_title(raw_body, remove=False):
        title = raw_body.find('h1')
        return title.decompose() if remove else title.get_text(strip=True)

    @staticmethod
    def extract_author(node):
        author_node = node.find('a')

        if author_node:
            author_name = author_node.get_text()
            author_url = author_node.get('href')
        else:
            author_name = node.get_text()
            author_url = ""
        return {
            'author_name': author_name,
            'author_url': author_url,
        }

    @staticmethod
    def extract_description(node):
        desc_raw = node.find('meta', property="og:description").get('content')
        return re.sub(r'http[^ \n]+', '', desc_raw).strip()

    @staticmethod
    def extract_pagination(html, link):
        pagination = html.find('a', text=re.compile(r'Продолжение.?'))
        if not pagination:
            link_reg = re.search(r'telegra.ph/([^ -]+)', link).group(1)
            pagination_arr = html.find_all('a', href=re.compile(re.escape(link_reg)))
            pagination = pagination_arr[-1] if pagination_arr else None

        return pagination

    @staticmethod
    def parse_page(html_content, ex_data=None, previous_url=''):
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            article_html = soup.find('article')
            additional = article_html.find('address')
            date = soup.find('time').get('datetime')
            author_data = PageParser.extract_author(additional) if additional else None
            description = PageParser.extract_description(soup)
            link = soup.find('link', rel="canonical").get('href')
            if not article_html:
                raise ValueError("No article found in the HTML content")

            pagination_link = PageParser.extract_pagination(article_html, link)
            if pagination_link:
                next_page_url = pagination_link.get('href')
                pagination_link.decompose()
            previous_page_link = article_html.find('a', string=re.compile(r'.*Предыдущая часть.*'))
            if previous_page_link:
                previous_page_link.decompose()
            article_body = PageParser.parse_body(article_html.prettify().strip())
            if ex_data:
                # For subsequent pages: remove title and concatenate new body
                body = ex_data['body'] + article_body
            else:
                # For the first page: include title and body
                title = PageParser.find_title(article_html)
                body = article_body
            data = {
                "body": body,
                "title": ex_data['title'] if ex_data else title,
                "page": ex_data['page'] + 1 if ex_data else 1,
                "author": ex_data['author'] if ex_data else author_data,
                "date_published": date,
                "description": ex_data['description'] if ex_data else description
            }
            # Check for pagination link to next page
            if pagination_link and re.search(re.escape(next_page_url), previous_url) is None:
                if not next_page_url.startswith('http'):
                    next_page_url = 'https://telegra.ph' + next_page_url
                logging.info(f"Fetching next page: {next_page_url}")

                next_page_content = PageParser.fetch_page(next_page_url)
                if next_page_content:
                    print('Processing next page', next_page_url)
                    return PageParser.parse_page(next_page_content, ex_data=data, previous_url=link)
                else:
                    logging.error(f"Failed to fetch or parse next page: {next_page_url}")
            else:
                logging.info("No more pages found, ending pagination.")
            return data
        except Exception as e:
            logging.error(f"Error parsing page: {str(e)}")
            return ex_data if ex_data else {"body": "", "title": "", "page": 1}
