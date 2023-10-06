from . import *

import re

PAGE_BLACK_LIST = r'(twitter|facebook|instagram|paypal|linkedin)\.com|.*\.php.*\?'

def get_absolute(curr_url, url):
    parsed_url = urlparse(url)
    if not bool(parsed_url.netloc):
        parsed_url = urljoin(curr_url, url)
        return parsed_url
    return urlunparse(parsed_url)

def is_blacklisted(url, base_url):
    black_list = PAGE_BLACK_LIST
    result = urlparse(url)
    # check with black list
    if re.search(black_list, url):
        return True
    # check if netloc is equal to base_url
    # if not equal then it is an external link and is blacklisted
    return not urlparse(base_url).netloc == result.netloc
    # try:
    #     return not bool(result.netloc)
    # except ValueError:
    #     return True
    
def clean_url(url):
    url = re.sub(r'^(https?://)?(www\.)?', '', url)
    return url.replace('/', '_')