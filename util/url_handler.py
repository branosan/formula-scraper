from . import *

def get_absolute(curr_url, url):
    parsed_url = urlparse(url)
    # print(f'UTIL: {parsed_url}')
    if not bool(parsed_url.netloc):
        parsed_url = urljoin(curr_url, url)
        return parsed_url
    return urlunparse(parsed_url)

def is_blacklisted(url):
    black_list = r'(twitter|facebook|instagram).com'
    result = urlparse(url)
    if re.search(black_list, result.netloc):
        return True
    try:
        return not bool(result.netloc)
    except ValueError:
        return True