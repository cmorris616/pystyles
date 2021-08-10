import json
import logging
import re

from bs4 import BeautifulSoup


class StyleReader:
    _soup: BeautifulSoup
    _features = 'html5lib'

    def __init__(self, soup: BeautifulSoup = None, html_text: str = None, html_file_path: str = None):

        if soup is not None:
            self._soup = soup
        elif html_text is not None and html_text.strip() != "":
            self._soup = BeautifulSoup(html_text, features=self._features)
        elif html_file_path is not None and html_file_path.strip() != "":
            with open(html_file_path, 'r') as html_file:
                self._soup = BeautifulSoup(html_file.read(), self._features)

        self.read_page_styles()

    def read_page_styles(self):
        if self._soup is None:
            logging.warning("Cannot read page styles before parsing document")
            return

        if self._soup.style is None:
            return

        style_text = self._soup.style.string

        style_text = style_text.replace('\n', '')
        style_text = re.sub('^[ ]+', '"', style_text)
        style_text = re.sub('[ ]+$', '', style_text)
        style_text = re.sub('[ ](?={)', '', style_text)
        style_text = re.sub('{', '":{', style_text)
        style_text = re.sub('{[ ]+', '{"', style_text)
        style_text = re.sub(':[ ]+', '":"', style_text)
        style_text = re.sub(';[ ]+', ';"', style_text)
        style_text = re.sub(';"[^,}]', ';","', style_text)
        style_text = re.sub('[ ]+', ' ', style_text)
        style_text = re.sub('}[ ]+', '},"', style_text)
        style_text = re.sub('[ ]+{', '":{', style_text)
        style_text = "{" + style_text + "}"

        style_dict = json.loads(style_text)

        split_keys = []

        # Selector and list of styles

        for key in style_dict.keys():
            if ',' in key:
                split_keys.append(key)

        for split_key in split_keys:
            new_key_array = split_key.split(',')
            value = style_dict[split_key]

            for new_key in new_key_array:
                style_dict[new_key] = value

            del style_dict[split_key]
