from . import *

PUNCTUATION = r'[^\w\s’]'

def create_tfidf(dir='./data/https:/pitwall.app/races'):
    file_structure = list(os.walk(dir, topdown=True))
    structure_size = len(file_structure)
    # contains tuples of (path, files content)
    corpus = []
    print('[1/2]Reading files...')
    for n, (path, dirs, files) in enumerate(file_structure):
        # skip if already processed
        if 'page.txt' in files:
            try:
                with open(f'{path}/page.txt', 'r', encoding='utf-8') as f:
                    print(f'Document: {n}/{structure_size}', end='\r')
                    doc = f.read()
                    words = clean_text(doc)
                    corpus.append((f'{path}/page.txt', words))
            except:
                print(f'ERROR {path}')
    print('')
    print('[DONE]')
    
    print('[2/2]Computing tf...', end='\r')
    # TODO commented to simplify indexing
    # tf_documents = [(path, compute_tf(words)) for path, words in corpus]
    tf_documents = {}
    for path, words in corpus:
        print(f'Computing tf for: {path}')
        tf_documents[path] = compute_tf(words)

    with open('./backup/tf.json', 'w') as json_file:
            json.dump(tf_documents, json_file) 
    print('')
    print('[DONE]')

    # END HERE
    # TODO commented to simplify indexing
    # print('[3/4]Computing idf...')
    # idf = {}
    
    # total_len = len(corpus)
    # i = 0

    # for path, words in corpus:
    #     i += 1
    #     print(f'Document: {i}/{total_len}', end='\r')
    #     for word in words:
    #         idf[word] = compute_idf(corpus, word)
    
    # with open('./backup/idf.json', 'w') as json_file:
    #         json.dump(idf, json_file)
    # print('')
    # print('[DONE]')
    
    # print('[4/4]Computing tf-idf...')
    # # tfidf_documents contains
    # # { 
    # #   <path>: {<word>: tfidf_value, ...},
    # #  ...
    # # }
    # i = 0
    # tfidf_documents = {}
    # for path, tf in tf_documents:
    #     tfidf_dict = {}

    #     i += 1
    #     print(f'Document: {i}/{total_len}', end='\r')

    #     for word, tf_value in tf.items():
    #         idf_value = idf.get(word, 0)
    #         tfidf_value = tf_value * idf_value
    #         tfidf_dict[word] = tfidf_value
    #     tfidf_documents[path] = tfidf_dict
    # print('[DONE]')

    # print('Writing tf-idf to file...')
    # with open('./backup/tfidf.json', 'w') as json_file:
    #         json.dump(tfidf_documents, json_file)
    # with open('./backup/idf.json', 'w') as json_file:
    #         json.dump(idf, json_file)

def lookup_document(prompt):
    # compute tf for the prompt
    tf_prompt = compute_tf(clean_text(prompt))
    idf = {}
    tf_documents = {}
    # TODO commented to simplify indexing
    # with open('./backup/tfidf.json', 'r') as json_file:
    #     tfidf_documents = json.load(json_file)
    # with open('./backup/idf.json', 'w') as json_file:
    #         idf = json.load(json_file)
    with open('./backup/tf.json', 'r') as json_file:
        tf_documents = json.load(json_file)

    # TODO commented to simplify indexing
    # tfidf_prompt = {}
    # for word, tf in tf_prompt.items():
    #     idf_value = idf.get(word, 0)
    #     tfidf_prompt[word] = tf * idf_value

    similarities = [(path, cosine_similarity(tf_prompt, tf_doc)) for path, tf_doc in tf_documents.items()]
    # TODO commented to simplify indexing
    # similarities = [(path, cosine_similarity(tfidf_prompt, tfidf_doc)) for path, tfidf_doc in tfidf_documents.items()]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:10]


def clean_text(text):
    return re.sub(PUNCTUATION, ' ', text).split()

def compute_tf(words):
    doc_size = len(words)
    tf = {}
    for word in words:
        tf[word] = tf.get(word, 0) + 1
    for (word, count) in tf.items():
        tf[word] = count / doc_size
    return tf

def compute_idf(corpus, word):
    num_docs_with_word = sum([1 for _, doc in corpus if word in doc])
    if num_docs_with_word > 0:
        return math.log(len(corpus) / num_docs_with_word)
    else:
        return 0
    
def cosine_similarity(v1, v2):
    dot_prod = sum(v1.get(word, 0) * v2.get(word, 0) for word in set(v1.keys()) & set(v2.keys()))
    mag_1 = math.sqrt(sum(val ** 2 for val in v1.values()))
    mag_2 = math.sqrt(sum(val ** 2 for val in v2.values()))
    if mag_1 == 0 or mag_2 == 0:
        return 0
    return dot_prod / (mag_1 * mag_2)
