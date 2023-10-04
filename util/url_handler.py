from . import *

def get_absolute(curr_url, url):
    parsed_url = urlparse(url)
    if not bool(parsed_url.netloc):
        parsed_url = urljoin(curr_url, url)
        print(f'URL_HANDLER: {parsed_url}')
        return parsed_url
    return urlunparse(parsed_url)