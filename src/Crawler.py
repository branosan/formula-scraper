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
        queue = [[self.url, 0]]
        # load queue from backup file
        try:
            queue = self.load_queue()
            visited = self.load_visited()
        except FileNotFoundError:
            log(['No queue/visited backup found. Starting from scratch...'])

        # BFS algorithm
        try:
            while queue:
                target, depth = queue.pop(0)
                if depth > self.max_depth:
                    continue

                if target in visited:
                    continue

                # request website
                try:
                    self.driver.get(target)
                    time.sleep(1)
                    # scroll to the bottom of the page
                    try:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    except WebDriverException as we:
                        log([f'Exception: {we}', f'Could not scroll to bottom of page: {target}'])
                    
                    soup = bs(self.driver.page_source, 'html.parser')
                    
                    os.makedirs(f"data/{target}", exist_ok=True)
                    with (open(f'./data/{target}/page.txt', 'w')) as f:
                        f.write(target + '\n')
                        f.write(str(soup))
                    visited.add(target)
                except ConnectionError:
                    log([f'Host {target} could not be resolved. Skipping host.'])
                    continue
                
                # find all hrefs and put them into a list
                links = find_links(soup)
                # iterate through all links and add them to the queue
                for link in links:
                    abs_url = get_absolute(target, link)
                    if is_blacklisted(abs_url, self.url):
                        continue
                    # branch off to wikipedia pages
                    if is_gp(abs_url):
                        gp_year_name = abs_url.split('/')[-1]
                        # convert string to words separated by underscores and capitalize each word
                        gp_name = '_'.join(gp_year_name.split('-')[1:]).title()
                        wiki_gp_url = f'https://en.wikipedia.org/wiki/{gp_name}'
                        if wiki_gp_url not in visited:
                            queue.append([wiki_gp_url, 0])
                    if abs_url not in visited:
                        queue.append([abs_url, depth + 1])
                log([f'Visited {target}', f'Queue size: {len(queue)}'])
            print('Max depth reached. Closing driver...')
            self.driver.quit()
        except KeyboardInterrupt:
            log(['KeyboardInterrupt'])
            print('Closing driver...')
            self.driver.quit()
            print('Backing up queue...')
            self.backup_queue(queue)
            print('Backing up Visisted...')
            self.backup_visited(visited)
            print('Exiting...')
        # any other exception    
        except Exception as e:
            log(['Unknown error', f'Exception {e}'])
            print('Closing driver...')
            self.driver.quit()
            print('Backing up queue...')
            self.backup_queue(queue)
            print('Backing up Visisted...')
            self.backup_visited(visited)
            print('Exiting...')
            exit(1)

    def text_from_html(self, s):
        texts = s.get_text()
        return re.sub(r'[\s\r\n]+', ' ', texts)
    
    def backup_queue(self, queue):
        with open('./backup/queue.json', 'w') as json_file:
            json.dump(queue, json_file)
    
    def load_queue(self):
        with open('./backup/queue.json', 'r') as json_file:
            loaded_queue = json.load(json_file)
        return loaded_queue
    
    def backup_visited(self, visited):
        with open('./backup/visited.json', 'w') as json_file:
            json.dump(visited, json_file)
    
    def load_visited(self):
        with open('./backup/visited.json', 'r') as json_file:
            loaded_visited = json.load(json_file)
        return loaded_visited