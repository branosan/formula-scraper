from . import *

if __name__ == '__main__':
    # https://pitwall.app/seasons
    # https://www.wikiwand.com/en/Formula_One
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')
    max_depth = int(sys.argv[1])
    curr_url = sys.argv[2]
    os.makedirs('./data', exist_ok=True)
    
    crawler = Crawler(curr_url, max_depth)
    crawler.crawl()
    # construct blacklist for this crawler

# TODO plan
#   Each website will be used to list all links which will be added to a queue.
#   We will iterate through the queue to visit all websites
#   make a table with words their frequency and code of ducment in which the words is located
#   implement potrer - reduce all words to their stems == easier look up

# TODO 
# natahat html zo vsetkych stranok nemenit ich
# vytvorit index z html
# otazky:
# - 
# vybrat entity ktore nas zaujimaju napriklad jazdci a okruhy na ktorych vyhrali
# pouzit paralelizovane vypocty na skratenie casu
# pre kazdy crawlnuty dokument si chceme vytvorit vector v priestore