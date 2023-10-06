from . import *

import re

PAGE_BLACK_LIST = r'(twitter|facebook|instagram).com'

def get_absolute(curr_url, url):
    parsed_url = urlparse(url)
    if not bool(parsed_url.netloc):
        parsed_url = urljoin(curr_url, url)
        return parsed_url
    return urlunparse(parsed_url)

def is_blacklisted(url):
    black_list = PAGE_BLACK_LIST
    result = urlparse(url)
    if re.search(black_list, result.netloc):
        return True
    try:
        return not bool(result.netloc)
    except ValueError:
        return True
    
def clean_url(url):
    url = re.sub(r'^(https?://)?(www\.)?', '', url)
    return url.replace('/', '_')