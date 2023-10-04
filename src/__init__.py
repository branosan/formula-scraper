from bs4 import BeautifulSoup as bs
import requests
from util.url_handler import get_absolute, is_blacklisted
from requests.exceptions import ConnectionError