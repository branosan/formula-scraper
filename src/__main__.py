from . import *
import lucene
from .indexer import create_tfidf, lookup_document
from .pylucene_indexer import create_index, basic_search, search_for_drivers, search_bad_weather, find_controversies
from .queries import find_wins, find_most_wins, find_collegues, find_dnfs, join_controversy_context
from .xml_parser import join_data

PATH_TO_PARSED_WIKI = './data/results'

def clear_screen():
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')


def get_text():
    # DEPRECATED
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
    # create folder where csv will be stored if it doesn't already exist
    os.makedirs('./data/procesed_data/', exist_ok=True)
    output = open('./data/procesed_data/entities.csv', 'w')

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

if __name__ == '__main__':
    # https://pitwall.app/seasons
    # https://www.wikiwand.com/en/Formula_One
    lucene.initVM()
    os.makedirs('./data', exist_ok=True)
    while True:
        clear_screen()
        argv = input('''
=========================Menu===========================
[c] Launch crawler "c <max_depth> <url>"
[s] Full text search "s <string>"
--------------------Called only once--------------------
[p] Create PyLucene index     
[j] Join data from csv and json files           
[e] Create csv file with entities              
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

        elif argv[0].lower() == 'p':
            create_index()
            _ = input('Press ENTER to continue...')

        elif argv[0].lower() == 'j':
            join_data(wiki_folder=PATH_TO_PARSED_WIKI, csv_file='./data/procesed_data/df_entities.csv')
            print('Joining data finished')
            _ = input('Press ENTER to continue...')

        elif argv[0].lower() == 's':
            choice = input('''
    [1] Find when two pilots met in a grand prix
    [2] Find GPs with bad weather and count DNFs
    [3] Find the most controversial GPs and pilots
    [4] Basic search
:''')
            if choice == '1':
                p1 = input('Enter name of the first pilot: ').lower()
                p2 = input('Enter name of the second pilot: ').lower()
                try:
                    year = input('Enter year year: ')
                except ValueError:
                    print('Invalid command check if year is written correctly', end='\r')
                    time.sleep(2)
                    continue
                files = search_for_drivers(p1, p2, year)
                wins_dict = find_wins(p1, p2, files)
                
                # print results
                print(f'\n{p1.title()} and {p2.title()} met during:')
                for key, value in wins_dict.items():
                    print('-'*30)
                    print(f'{key}')
                    _ = [print(f'{k}: {v}') for k, v in value.items()]
            elif choice == '2':
                years = input('Enter year year range [<year1> <year2>]: ')
                weather = input('Enter weather condition: ')
                min_dnfs = int(input('Enter minimum number of DNFs: '))
                files = search_bad_weather(weather, years)
                dnfs_dict = find_dnfs(files, min_dnfs)
                # print results
                years = years.split(' ')
                print(f'\nBetween {years[0]}-{years[1]} it was {weather} on:')
                for key, value in dnfs_dict.items():
                    print('='*10 + f'{key}' + '='*10)
                    print(f'DNFs = {value}')
            
            elif choice == '3':
                years = input('Enter year year range [<year1> <year2>]: ')
                files = find_controversies(years)
                result_dict = join_controversy_context(files)
                # print results
                years = years.split(' ')
                for gp, value in result_dict.items():
                    print('='*10 + f'{gp}' + '='*10)
                    print(f'Controversy: {value["context"]}')
                    if value.get('drivers') is None:
                        print('No drivers found in records...')
                        continue
                    _ = [print(f'{k}: {v}') for k, v in value['drivers'].items()]
            elif choice == '4':
                query = input('Enter query: ')
                basic_search(query)
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