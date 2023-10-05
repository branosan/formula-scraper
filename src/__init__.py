from bs4 import BeautifulSoup as bs
from bs4.element import Comment
import requests
from util.url_handler import get_absolute, is_blacklisted
from requests.exceptions import ConnectionError
import sys
import re