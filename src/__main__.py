from . import *

if __name__ == '__main__':
    # https://pitwall.app/
    # https://www.wikiwand.com/en/Formula_One
    max_depth = int(sys.argv[1])
    curr_url = sys.argv[2]
    os.makedirs('./data', exist_ok=True)
    
    crawler = Crawler(curr_url, max_depth)
    crawler.crawl()
    # construct blacklist for this crawler


    # main(curr_url, max_depth)

# TODO plan
#   Each website will be used to list all links which will be added to a queue.
#   We will iterate through the queue to visit all websites
#   make a table with words their frequency and code of ducment in which the words is located
#   implement potrer - reduce all words to their stems == easier look up

# contents of target page
# check if page is for a f1 circuit (contains "-grand-prix")
# if it does contain grand prix find wiki page for this grand-prix by modifing current xxx-grand-prix to
# Xxx_Grand_Prix and concat with wikipedia page