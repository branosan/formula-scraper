from . import *
import sys
import os
from pathlib import Path
import lucene
from java.io import StringReader
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, StringField, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, Term, IndexOptions
from org.apache.lucene.search import IndexSearcher, Query, TermQuery, BooleanQuery, BooleanClause, FuzzyQuery, WildcardQuery, TermRangeQuery
from org.apache.lucene.store import NIOFSDirectory, FSDirectory
from org.apache.lucene.queryparser.classic import QueryParser

INDEX_PATH = './pylucene_index'
DOC_ID_KEY = 'id'

BAD_WEATHER_TERMS = [
    'rain',
    'torrential',
    'cloudy',
    'wet',
    'storm',
    'collision',
    'rain-soaked',
    'soaked'
]

CONTROVERSY_TERMS = [
    'controversy',
    'unsafe',
    'outrage',
]

def create_index(dir='./data/results'):
    print('-----------------------------------')
    print(f'Using lucene {lucene.VERSION}')
    print('-----------------------------------')
    os.makedirs(INDEX_PATH, exist_ok=True)

    # # load files to index
    # files = os.listdir(dir)
    # files_size = len(files)

    file_structure = list(os.walk(dir, topdown=True))
    structure_size = len(file_structure)

    # lucene.initVM()

    # Create an Analyzer (use StandardAnalyzer for text indexing)
    analyzer = StandardAnalyzer()

    # Create an IndexWriterConfig with the specified analyzer
    config = IndexWriterConfig(analyzer)

    # Specify the directory where you want to create the index
    index_directory = NIOFSDirectory(Paths.get(INDEX_PATH))

    # tokenized weather query
    string_field_tokenized = FieldType()
    string_field_tokenized.setStored(False)
    string_field_tokenized.setTokenized(True)
    string_field_tokenized.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)

    writer = IndexWriter(index_directory, config)

    for n, (path, dirs, files) in enumerate(file_structure):
        print(f'{n}/{structure_size}', end='\r')
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(path, filename)
                # load all files in the data directory
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
        
                document = Document()
                document.add(Field(DOC_ID_KEY, file_path, TextField.TYPE_STORED))
                # add names to the index
                for d in json_data['results']:
                    name = d['DRIVER NAME']
                    # get rid of leading driver number in the name
                    name = ' '.join(name.split()[1:])
                    document.add(StringField('driver', name, Field.Store.YES))
                document.add(Field('year', json_data['YEAR'], TextField.TYPE_NOT_STORED))
                document.add(Field('weather', json_data['WEATHER'], string_field_tokenized))
                document.add(Field('title', json_data['title'], TextField.TYPE_NOT_STORED))
                document.add(Field('content', json_data['text'], TextField.TYPE_NOT_STORED))
                writer.addDocument(document)
                # commit every 200 documents
                writer.commit() if n % 200 == 0 else None

    writer.commit()
    writer.close()
    index_directory.close()
    print('Finished creating index')

def basic_search(phrase):
    # lucene.initVM()
    print('-----------------------------------')
    print(f'Using lucene {lucene.VERSION}')
    print('-----------------------------------')
    reader = DirectoryReader.open(FSDirectory.open(Paths.get(INDEX_PATH)))
    searcher = IndexSearcher(reader)

    # Split the phrase into two words
    words = phrase.split()

    # Create a BooleanQuery with both words as MUST clauses
    boolean_query = BooleanQuery.Builder()
    for word in words:
        term_query = TermQuery(Term("content", word))
        boolean_query.add(term_query, BooleanClause.Occur.MUST)

    query = boolean_query.build()

    top_docs = searcher.search(query, 10)

    print(f'Search results for "{phrase}":')
    for score_doc in top_docs.scoreDocs:
        # retriev id which pylucene assigned to document
        lucene_doc_id = score_doc.doc
        doc = searcher.doc(lucene_doc_id)
        # get my own file identificator
        id_field = doc.get(DOC_ID_KEY)
        print(f'Document ID: {id_field}')

    reader.close()

def search_for_drivers(d1, d2, year, results_n=10):
    """
    Builds a query which find if two drivers have met in specified year.
    
    Query: 
        title: (year && .* && grand && prix)
        &&
        content: (driver1 && driver2)
    """
    print('-----------------------------------')
    print(f'Using lucene {lucene.VERSION}')
    print('-----------------------------------')
    reader = DirectoryReader.open(FSDirectory.open(Paths.get(INDEX_PATH)))
    searcher = IndexSearcher(reader)

    boolean_query = BooleanQuery.Builder()

    # Find grand prix from the time period
    # handle year
    year_query = TermRangeQuery.newStringRange('year', year, year, True, True)
    boolean_query.add(year_query, BooleanClause.Occur.MUST)

    for driver_name in [d1, d2]:
        query = FuzzyQuery(Term('driver', driver_name), 2)
        boolean_query.add(query, BooleanClause.Occur.MUST)

    query = boolean_query.build()
    top_docs = searcher.search(query, results_n)

    # extract paths to json files from the top_docs
    paths = [searcher.doc(score_doc.doc).get(DOC_ID_KEY) for score_doc in top_docs.scoreDocs]
    print(paths)
    reader.close()
    return paths

def search_bad_weather(weather, year_range, results_n=10):
    """
    Builds a query which looks for a grand prix with bad weather.
    This will be later connected with my crawled csv file from which the number of
    drivers who DNF-ed will be extracted.
    
    Query:
        title: (year(from range) && .* && grand && prix)
        &&
        content: (word1 || word2 || ... || wordN)
    """
    print('-----------------------------------')
    print(f'Using lucene {lucene.VERSION}')
    print('-----------------------------------')
    
    years = year_range.split(' ')

    reader = DirectoryReader.open(FSDirectory.open(Paths.get(INDEX_PATH)))
    searcher = IndexSearcher(reader)

    boolean_query = BooleanQuery.Builder()
    # Find grand prix from the time period
    year_query = TermRangeQuery.newStringRange('year', years[0], years[1], True, True)
    boolean_query.add(year_query, BooleanClause.Occur.MUST)

    weather_sub_query = BooleanQuery.Builder()
    # Build query for page content
    for token in weather.split():
        fuzzy_query = FuzzyQuery(Term('weather', token), 2)
        weather_sub_query.add(fuzzy_query, BooleanClause.Occur.SHOULD)
    
    boolean_query.add(weather_sub_query.build(), BooleanClause.Occur.MUST)
    query = boolean_query.build()
    top_docs = searcher.search(query, results_n)
    
    paths = [searcher.doc(score_doc.doc).get(DOC_ID_KEY) for score_doc in top_docs.scoreDocs]
    reader.close()
    return paths

def find_controversies(year_range, results_n=10):
    """
    Finds GPs within the specified time period which were controversial.

    Query:
        title: ((year && .* && grand && prix) || (year && .* && grand && prix))
        &&
        content: (word1 || word2 || ... || wordN)
    """
    
    print('-----------------------------------')
    print(f'Using lucene {lucene.VERSION}')
    print('-----------------------------------')
    
    years = year_range.split(' ')

    reader = DirectoryReader.open(FSDirectory.open(Paths.get(INDEX_PATH)))
    searcher = IndexSearcher(reader)

    boolean_query = BooleanQuery.Builder()
    title_sub_query = BooleanQuery.Builder()

    # Build query for title
    for year in range(int(years[0]), int(years[1])+1):
        title_pattern = f'{year} * Grand Prix'.lower().split()
        # handle year
        sub_sub_query = BooleanQuery.Builder()
        year_term = TermQuery(Term('title', title_pattern[0]))
        sub_sub_query.add(year_term, BooleanClause.Occur.MUST)
        # handle wildcard "*"
        wildcard_sub_quer = WildcardQuery(Term('title', f'{title_pattern[1]}'))
        sub_sub_query.add(wildcard_sub_quer, BooleanClause.Occur.MUST)
        # handle "grand prix" term
        for term in title_pattern[2:]:
            title_term = TermQuery(Term('title', term))
            sub_sub_query.add(title_term, BooleanClause.Occur.MUST)

        title_sub_query.add(sub_sub_query.build(), BooleanClause.Occur.SHOULD)
    boolean_query.add(title_sub_query.build(), BooleanClause.Occur.MUST)

    content_sub_query = BooleanQuery.Builder()

    for term in CONTROVERSY_TERMS:
        # Use FuzzyQuery to find similar terms
        fuzzy_query = FuzzyQuery(Term('content', term), 2)
        content_sub_query.add(fuzzy_query, BooleanClause.Occur.SHOULD)
    boolean_query.add(content_sub_query.build(), BooleanClause.Occur.MUST)

    query = boolean_query.build()
    top_docs = searcher.search(query, results_n)

    paths = [searcher.doc(score_doc.doc).get(DOC_ID_KEY) for score_doc in top_docs.scoreDocs]
    reader.close()
    return paths