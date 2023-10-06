from bs4 import BeautifulSoup as bs
from bs4.element import Comment
from urllib.parse import urlparse, urlunparse
from urllib.parse import urljoin
import requests
from requests.exceptions import ConnectionError
import sys
import re
import os

from src.url_handler_scripts import get_absolute, is_blacklisted, clean_url
from .Crawler import Crawler