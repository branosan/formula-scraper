from . import *

class Crawler:

    def __init__(self, url, max_depth):
        self.url = url
        self.max_depth = max_depth
        self.load_index = 0

        # initialize selenium driver
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def crawl(self):
        visited = set()
        queue = [(self.url, 0)]
        try:
            while queue:
                target, depth = queue.pop(0)
                
                if depth > self.max_depth:
                    continue
                
                if target in visited:
                    continue

                try:
                    self.driver.get(target)
                    time.sleep(0.5)
                    # scroll to the bottom of the page
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    soup = bs(self.driver.page_source, 'html.parser')
                    with (open(f'./data/{depth}__{clean_url(target)}.txt', 'w')) as f:
                        f.write(target + '\n')
                        f.write(self.text_from_html(soup))
                    visited.add(target)
                except ConnectionError:
                    print(f'Host {target} could not be resolved. Skipping host.')
                    continue
                # find all hrefs and put them into a list
                links = [a.get('href') for a in soup.find_all('a', href=True)]

                # iterate through all links and add them to the queue
                for link in links:
                    self.loading_screen()
                    abs_url = get_absolute(target, link)
                    if is_blacklisted(abs_url, self.url):
                        continue
                    if abs_url not in visited:
                        queue.append((abs_url, depth + 1))
                    # branch off to wikipedia pages
                    if is_gp(abs_url):
                        gp_year_name = abs_url.split('/')[-1]
                        # convert string to words separated by underscores and capitalize each word
                        gp_name = '_'.join(gp_year_name.split('-')[1:]).title()
                        wiki_gp_url = f'https://en.wikipedia.org/wiki/{gp_name}'
                        if wiki_gp_url not in visited:
                            queue.append((wiki_gp_url, depth + 1))
                time.sleep(0.5)
            self.driver.quit()
        except KeyboardInterrupt:
            print('\n')
            print('Closing driver...')
            self.driver.quit()
            print('Closing crawler...')
            print('Exiting...')
        # any other exception    
        except Exception as e:
            print(f'Error occurted: {e}')
            print('\n')
            print('Closing driver...')
            self.driver.quit()
            print('Closing crawler...')
            print('Exiting...')
            exit(0)

    def loading_screen(self):
        charset = ['|', '/', '-', '\\']
        print('Crawliing...', end='')
        i = self.load_index % (len(charset) - 1)
        print(charset[i], end='\r')
        self.load_index += 1

    def text_from_html(self, s):
        texts = s.get_text()
        return re.sub(r'[\s\r\n]+', ' ', texts)