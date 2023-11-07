import sys
import os
from pathlib import Path
import lucene
from java.io import StringReader
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import NIOFSDirectory


def test_index():
    print(lucene.VERSION)
    index_path = "./pylucene_index"
    if not os.path.exists(index_path):
        os.makedirs(index_path)

    lucene.initVM()

    # Create an Analyzer (use StandardAnalyzer for text indexing)
    analyzer = StandardAnalyzer()

    # Create an IndexWriterConfig with the specified analyzer
    config = IndexWriterConfig(analyzer)

    # Specify the directory where you want to create the index
    index_directory = NIOFSDirectory(Paths.get(index_path))

    writer = IndexWriter(index_directory, config)

    documents = []
    doc_path = 'data/https:/en.wikipedia.org/wiki/1992_Canadian_Grand_Prix/page.txt'
    with open(doc_path, 'r', encoding='utf-8') as f:
        doc = f.read()
        documents.append({'id': doc_path, 'content': doc})
    
    for doc in documents:
        document = Document()
        document.add(Field('id', doc['id'], TextField.TYPE_STORED))
        document.add(Field('content', doc['content'], TextField.TYPE_STORED))
        writer.addDocument(document)

    writer.close()
    print('Finished creating index')

test_index()