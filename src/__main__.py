from . import *

def main(curr_url, max_depth):
    visited = set()
    # queue for BFS
    queue = [(curr_url, 0)]
    while queue:
        # TODO check for already visited websites
        target, depth = queue.pop(0)
        
        if depth > max_depth:
            continue

        if target not in visited:
            try:
                # contents of target page
                page = requests.get(target)
                soup = bs(page.text, 'html.parser')
                visited.add(target)
            except ConnectionError:
                print(f'Host {target} could not be resolved. Skipping host.')
                continue
            # find all hrefs and put them into a list
            links = [a.get('href') for a in soup.find_all('a', href=True)]

            for link in links:
                abs_url = get_absolute(target, link)
                if is_blacklisted(abs_url):
                    continue
                queue.append((abs_url, depth + 1))



if __name__ == '__main__':
    curr_url = sys.argv[1]
    max_depth = 10
    main(curr_url, max_depth)

# TODO plan
#   Each website will be used to list all links which will be added to a queue.
#   We will iterate through the queue to visit all websites
#   make a table with words their frequency and code of ducment in which the words is located
#   implement potrer - reduce all words to their stems == easier look up