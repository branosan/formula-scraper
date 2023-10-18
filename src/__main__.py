from . import *

def clear_screen():
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')


def get_text():
    os.makedirs('./procesed_data', exist_ok=True)
    full_text = open('./procesed_data/fulltext.txt', 'a+')

    file_structure = list(os.walk('./data', topdown=True))
    structure_size = len(file_structure)

    for n, (path, dirs, files) in enumerate(file_structure):
        if 'page.txt' in files:
            try:
                with open(f'{path}/page.txt', 'r') as f:
                    print(f'{n}/{structure_size}\t{path}', end='\r')
                    content = bs(f.read(), 'html.parser')
                    full_text.write(content.get_text())
            except:
                print(f'ERROR {path}')
        

    full_text.close()

def find(pattern):
    # grep -i -r 'formula' ./data
    os.system(f'grep -i -r \'{pattern}\' ./fulltext.txt')

if __name__ == '__main__':
    # https://pitwall.app/seasons
    # https://www.wikiwand.com/en/Formula_One

    os.makedirs('./data', exist_ok=True)
    while True:
        clear_screen()
        argv = input('''
===============Menu===============
[c] Launch crawler "c <max_depth> <url>"
[s] Full text search "s <string>"
[t] Create full text file                        
[q] Quit
''')
        argv = argv.split(' ')
        if argv[0].lower() == 'c':
            try:
                max_depth = int(argv[1])
                curr_url = argv[2]
                crawler = Crawler(curr_url, max_depth)
                print('Launching crawler...')
                crawler.crawl()
            except IndexError:
                print('Invalid command', end='\r')
                time.sleep(2)
                continue
        elif argv[0].lower() == 't':
            print('Creating full text file...')
            get_text()
        elif argv[0].lower() == 'q':
            print('Quiting...')
            time.sleep(1)
            break
        else:
            print('Invalid command', end='\r')
            time.sleep(2)

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