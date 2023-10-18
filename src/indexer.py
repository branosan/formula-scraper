from . import *

def create_index():
    file_structure = list(os.walk('./data', topdown=True))
    structure_sz = len(file_structure)

    for n, (path, dirs, files) in enumerate(file_structure):
        pass

def search_index():
    pass


# def get_text():
#     full_text = open("fulltext.txt", "a+")

#     file_structure = list(os.walk('./data', topdown=True))
#     structure_size = len(file_structure)

#     for n, (path, dirs, files) in enumerate(file_structure):
#         if 'page.txt' in files:
#             try:
#                 with open(f'{path}/page.txt', 'r') as f:
#                     print(f'{n}/{structure_size}\t{path}', end='\r')
#                     content = bs(f.read(), 'html.parser')
#                     full_text.write(content.get_text())
#             except:
#                 print(f'ERROR {path}')
        

#     full_text.close()