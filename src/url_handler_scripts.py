from . import *

import re

PAGE_BLACK_LIST = r'(twitter|facebook|instagram|paypal|linkedin)\.com|/.*\.php.*|.+#.+'
BANNED_FILE_EXTENSIONS = r'(?<!\.(?:png))(?<!\.(?:css))(?<!\.(?:jpg))(?<!\.(?:gif))(?<!\.(?:js))(?<!\.(?:php))(?<!\.(?:bmp))(?<!\.(?:pdf))(?<!\.(?:docx))(?<!\.(?:jpeg))'
LINK_REGEX = r'href=[\"\'](https?://\S+|/\S+)' + BANNED_FILE_EXTENSIONS + r'\b[\"\']'
# better regex href=[\"\'](https?://\S+|/\S+).*[\"\']
# even better href=[\"\'](https?://\S+|/\S+)(?<!\.(?:png))(?<!\.(?:css))\b[\"\']
def get_absolute(curr_url, url):
    parsed_url = urlparse(url)
    if not bool(parsed_url.netloc):
        parsed_url = urljoin(curr_url, url)
        return parsed_url
    return urlunparse(parsed_url)

def find_links(soup):
    return re.findall(LINK_REGEX, str(soup))

def is_blacklisted(url, base_url):
    black_list = PAGE_BLACK_LIST
    result = urlparse(url)
    # check with black list
    if bool(re.search(black_list, url)):
        return True
    # check if netloc is equal to base_url
    # if not equal then it is an external link and is blacklisted
    return not urlparse(base_url).netloc == result.netloc

def clean_url(url):
    url = re.sub(r'^(https?://)?(www\.)?', '', url)
    return url.replace('/', '_')

def is_gp(url):
    gp_pattern = r'\/[0-9]+-[a-z,-]+-grand-prix$'
    if bool(re.search(gp_pattern, url)):
        return True
    else :
        return False