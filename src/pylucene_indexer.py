from . import *
import sys
import os
from pathlib import Path
import lucene
from java.io import StringReader
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, Term
from org.apache.lucene.search import IndexSearcher, Query, TermQuery, BooleanQuery, BooleanClause, FuzzyQuery, WildcardQuery
from org.apache.lucene.store import NIOFSDirectory, FSDirectory

INDEX_PATH = './pylucene_index'
DOC_ID_KEY = 'id'

def test_index(dir='data/wiki_dump/pages'):
    print('-----------------------------------')
    print(f'Using lucene {lucene.VERSION}')
    print('-----------------------------------')
    if not os.path.exists(INDEX_PATH):
        os.makedirs(INDEX_PATH)

    # load files to index
    files = os.listdir(dir)
    files_size = len(files)

    # lucene.initVM()

    # Create an Analyzer (use StandardAnalyzer for text indexing)
    analyzer = StandardAnalyzer()

    # Create an IndexWriterConfig with the specified analyzer
    config = IndexWriterConfig(analyzer)

    # Specify the directory where you want to create the index
    index_directory = NIOFSDirectory(Paths.get(INDEX_PATH))

    writer = IndexWriter(index_directory, config)

    for n, filename in enumerate(files):
        print(f'{n}/{files_size}', end='\r')
        if filename.endswith('.json'):
            file_path = os.path.join(dir, filename)
            # load all files in the data directory
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
    
            document = Document()
            document.add(Field(DOC_ID_KEY, file_path, TextField.TYPE_STORED))
            document.add(Field('title', json_data['title'], TextField.TYPE_NOT_STORED))
            document.add(Field('content', json_data['text'], TextField.TYPE_STORED))
            writer.addDocument(document)

    writer.close()
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

def search_for_drivers(d1, d2, year):
    """
    Builds a query which find if two drivers have met in specified year
    Query: 
        title: (year && .* && grand && prix)
        &&
        content: (driver1 && driver2)
    """
    # lucene.initVM()
    print('-----------------------------------')
    print(f'Using lucene {lucene.VERSION}')
    print('-----------------------------------')
    reader = DirectoryReader.open(FSDirectory.open(Paths.get(INDEX_PATH)))
    searcher = IndexSearcher(reader)

    title_pattern = f'{year} * Grand Prix'.lower().split()

    boolean_query = BooleanQuery.Builder()

    # Find grand prix from the time period
    # handle year
    title_sub_query = BooleanQuery.Builder()
    year_term = TermQuery(Term('title', title_pattern[0]))
    title_sub_query.add(year_term, BooleanClause.Occur.MUST)
    # handle wildcard
    wildcard_sub_quer = WildcardQuery(Term('title', f'{title_pattern[1]}'))
    title_sub_query.add(wildcard_sub_quer, BooleanClause.Occur.MUST)
    # handle "grand prix" term
    for term in title_pattern[2:]:
        title_term = TermQuery(Term('title', term))
        title_sub_query.add(title_term, BooleanClause.Occur.MUST)

    boolean_query.add(title_sub_query.build(), BooleanClause.Occur.MUST)

    for driver_name in [d1, d2]:
        # split names into multiple terms
        for part_name in driver_name.split(' '):
            fuzzy_query = FuzzyQuery(Term('content', part_name), 2)
            boolean_query.add(fuzzy_query, BooleanClause.Occur.MUST)

    query = boolean_query.build()
    top_docs = searcher.search(query, 10)

    # print(f'GP from the time period {year}\nWhere {d1} and {d2} raced each other:')
    # for score_doc in top_docs.scoreDocs:
    #     # retriev id which pylucene assigned to document
    #     lucene_doc_id = score_doc.doc
    #     doc = searcher.doc(lucene_doc_id)
    #     # get my own file identificator
    #     id_field = doc.get(DOC_ID_KEY)
    #     print(f'Document ID: {id_field}')

    # extract paths to json files from the top_docs
    paths = [searcher.doc(score_doc.doc).get(DOC_ID_KEY) for score_doc in top_docs.scoreDocs]
    reader.close()
    return paths