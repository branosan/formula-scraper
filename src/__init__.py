from bs4 import BeautifulSoup as bs
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlparse, urlunparse
from urllib.parse import urljoin
import requests
from requests.exceptions import ConnectionError
import sys
import re
import os
import time
import json
import math
import pandas as pd
import xml.etree.ElementTree as et

from src.url_handler_scripts import get_absolute, is_blacklisted, clean_url, is_gp, find_links
from src.loging import log
from .Crawler import Crawler

HEADERS = 'YEAR;GP NAME;POS;DRIVER NAME;TEAM NAME;LAP TIME;GRID;LAPS;POINTS'
GP_PATTERN = r'\/[0-9]+-[a-z,-]+-grand-prix$'