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
from org.apache.lucene.search import IndexSearcher, Query, TermQuery
from org.apache.lucene.store import NIOFSDirectory, FSDirectory

INDEX_PATH = './pylucene_index'
DOC_ID_KEY = 'id'

def test_index(dir='data/wiki_dump/pages'):
    print(f'Using lucene {lucene.VERSION}')
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
    print(f'Using lucene {lucene.VERSION}')
    reader = DirectoryReader.open(FSDirectory.open(Paths.get(INDEX_PATH)))
    searcher = IndexSearcher(reader)

    query = TermQuery(Term("content", phrase))

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