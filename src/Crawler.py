from . import *

class Crawler:

    def __init__(self, url, max_depth):
        self.url = url
        self.max_depth = max_depth
        self.load_index = 0

    def crawl(self):
        visited = set()
        queue = [(self.url, 0)]
        while queue:
            target, depth = queue.pop(0)
            
            if depth > self.max_depth:
                continue

            if target not in visited:
                try:
                    page = requests.get(target)
                    soup = bs(page.text, 'html.parser')
                    with (open(f'./data/{depth}__{clean_url(target)}.txt', 'w')) as f:
                        f.write(self.text_from_html(soup))
                    visited.add(target)
                except ConnectionError:
                    print(f'Host {target} could not be resolved. Skipping host.')
                    continue
                # find all hrefs and put them into a list
                links = [a.get('href') for a in soup.find_all('a', href=True)]

                for link in links:
                    self.loading_screen()
                    abs_url = get_absolute(target, link)
                    if is_blacklisted(abs_url):
                        continue
                    queue.append((abs_url, depth + 1))

    def loading_screen(self):
        charset = ['|', '/', '-', '\\']
        print('Crawliing...', end='')
        i = self.load_index % (len(charset) - 1)
        print(charset[i], end='\r')
        self.load_index += 1

    # taken from https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        # remove white spaces and new lines
        elif re.match(r"[\s\r\n]+", str(element)):
            return False
        return True
    
    # taken from https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
    def text_from_html(self, s):
        texts = s.findAll(string=True)
        visible_text = filter(self.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_text)