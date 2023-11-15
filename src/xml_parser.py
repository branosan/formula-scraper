from . import *

WIKI_DUMP_PATH = 'data/wiki_dump'

def parse_dump_stream():
    """
    Extract relevant information for search, such as page title and text, from the XML dump using streaming.
    """
    files = os.listdir(WIKI_DUMP_PATH)
    print('Parsing XML dump...')
    namespace = {'mw': 'http://www.mediawiki.org/xml/export-0.10/'}

    for xml_file in files:
        xml_file_path = os.path.join(WIKI_DUMP_PATH, xml_file)
        if not os.path.isfile(xml_file_path) or xml_file.startswith('.'):
            yield {'title': None, 'text': None}
            continue
        for event, elem in et.iterparse(xml_file_path, events=('start', 'end')):
            if event == 'start':
                # Process the start of an element
                pass
            elif event == 'end':
                # Process the end of an element
                if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
                    title = elem.find('./mw:title', namespace).text
                    text_element = elem.find('./mw:revision/mw:text', namespace)
                    text = text_element.text if text_element is not None else ''
                    yield {'title': title, 'text': text}

                    # Clear the element to free memory
                    elem.clear()

    print('[DONE]')

def extract_pages_xml_stream():
    """
    Extract singular pages from the XML file and create a separate file for each page using streaming.
    This can then be used to create an index for each page.
    """
    for page in parse_dump_stream():
        if (page['title'] is None) or (re.search(GP_PATTERN_WIKI, page['title']) is None):
            continue
        # curate the title to remove first Wikipedia: word and replace all / with -
        page['title'] = page['title'].replace('/', '-')
        page['year'] = int(page['title'].split()[0])
        page['gp_name'] = '-'.join(page['title'].split(' ')[1:]).lower()
        # combine with the csv from previous crawl
        df = pd.read_csv('data/procesed_data/df_entities.csv', sep=';')
        filtered = df[(df['YEAR'] == page['year']) & (df['GP NAME'] == page['gp_name'])]
        filtered = filtered.iloc[:, 2::]
        filtered.set_index('DRIVER NAME', inplace=True)
        wiki_merge = {**page, 'results': filtered.to_dict()}
        
        try:
            with open(f'data/merged/{page["title"]}.json', 'w') as f:
                json.dump(wiki_merge, f)
        except OSError:
            pass