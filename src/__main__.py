from . import *
from .indexer import create_tfidf, lookup_document

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
        if 'page.html' in files:
            try:
                with open(f'{path}/page.html', 'r') as f:
                    print(f'{n}/{structure_size}', end='\r')
                    content = bs(f.read(), 'html.parser')
                    full_text.write(content.get_text())
            except:
                print(f'ERROR {path}')
        

    full_text.close()

def create_documents():
    file_structure = list(os.walk('./data', topdown=True))
    structure_size = len(file_structure)
    for n, (path, dirs, files) in enumerate(file_structure):
        # skip if already processed
        if 'page.txt' in files:
            continue
        if 'page.html' in files:
            text_file = open(f'{path}/page.txt', 'w')
            try:
                with open(f'{path}/page.html', 'r') as f:
                    print(f'{n}/{structure_size}', end='\r')
                    content = bs(f.read(), 'html.parser')
                    text_file.write(content.get_text())
                    text_file.close()
            except:
                print(f'ERROR {path}')

def find_entities():
    output = open('./procesed_data/entities.csv', 'w')

    file_structure = list(os.walk('./data/https:/pitwall.app', topdown=True))
    structure_size = len(file_structure)
    # write a header for the csv file
    output.write(f'{HEADERS}\n')
    for n, (path, dirs, files) in enumerate(file_structure):
        # DEBUG OUTPUT
        print(f'{n}/{structure_size}', end='\r')
        if 'page.html' in files:
            try:
                with open(f'{path}/page.html', 'r') as f:
                    url = f.readline()
                    gp_id = re.search(GP_PATTERN, url)
                    # if a file is read which does not contain a gp page
                    if not gp_id:
                        continue
                    soup = bs(f.read(), 'html.parser')
                    table = soup.find('table', class_='data-table')
                    # [1:] so that <th> elements are not taken into for loop
                    for row in table.find_all('tr')[1:]:
                        # extract year of a grand prix
                        gp_year = gp_id.group(0).split('-')[0][1:]
                        # extract name of a grand prix
                        gp_name = '-'.join(gp_id.group(0).split('-')[1:])
                        output_list = [gp_year, gp_name]
                        # output.write(f'{gp_name.group(0)[1:]};')
                        for id, cell in enumerate(row.find_all('td')):
                            # remove white spaces from the cell 
                            cell_text = re.sub(r'\s+', ' ', cell.text)
                            cell_text = cell_text.strip()
                            # remove number of positions the pilot move up or down
                            if id == 0:
                                cell_text = cell_text.split(' ')[0]
                            # output.write(f'{cell_text};')
                            output_list.append(cell_text)
                        output.write(';'.join(output_list))
                        output.write('\n')
                    # output.write(str(table))
            except Exception as e:
                print(e)
                break
    output.close()

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
[d] Create documents for each hmtl file
[i] Create index
[f] Look for a pattern in the full text file                     
[e] Find entities                      
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
        elif argv[0].lower() == 'd':
            print('Creating documents...')
            create_documents()    
        elif argv[0].lower() == 'i':
            create_tfidf(dir='./data')
        elif argv[0].lower() == 'f':
            pattern = input('Enter a pattern: ')
            top_docs = lookup_document(pattern)
            # print top documents
            _ = [print(doc) for doc in top_docs]
            _ = input('Press ENTER to continue...')
        elif argv[0].lower() == 'e':
            find_entities()
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