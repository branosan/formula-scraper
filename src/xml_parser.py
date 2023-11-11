from . import *

def parse_dump_stream(xml_file='data/wiki_dump/enwiki-20230920-pages-articles-multistream2.xml-p41243p151573'):
    """
    Extract relevant information for search, such as page title and text, from the XML dump using streaming.
    """
    print('Parsing XML dump...')
    namespace = {'mw': 'http://www.mediawiki.org/xml/export-0.10/'}

    for event, elem in et.iterparse(xml_file, events=('start', 'end')):
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
        # curate the title to remove first Wikipedia: word and replace all / with -
        page['title'] = ' '.join(page['title'].split(' ')[1:]).replace('/', '-')
        with open(f'data/wiki_dump/pages/{page["title"]}.json', 'w') as f:
            json.dump(page, f)