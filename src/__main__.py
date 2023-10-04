from . import *

def main(curr_url):
    visited = set()
    # queue for BFS
    queue = [curr_url]
    while queue:
        # TODO check for already visited websites
        target = queue.pop(0)
        # contents of target page
        page = requests.get(target)
        soup = bs(page.text, 'html.parser')
        visited.add(target)
        # find all hrefs and put them into a list
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        for link in links:
            abs_url = get_absolute(target, link)
            sub_page = requests.get(abs_url)
            sub_soup = bs(sub_page.text, 'html.parser')
            sub_links = [a.get('href') for a in sub_soup.find_all('a', href=True)]
            # append new links to queue
            queue.extend(sub_links)



if __name__ == '__main__':
    curr_url ="https://pitwall.app/"
    main(curr_url)

# TODO plan
#   Each website will be used to list all links which will be added to a queue.
#   We will iterate through the queue to visit all websites
#   make a table with words their frequency and code of ducment in which the words is located
#   implement potrer - reduce all words to their stems == easier look up