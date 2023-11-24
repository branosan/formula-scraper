from . import *

def join_data(wiki_folder, csv_file):
    file_structure = list(os.walk(wiki_folder, topdown=True))
    structure_size = len(file_structure)
    df = pd.read_csv(csv_file, sep=';')
    for n, (path, dirs, files) in enumerate(file_structure):
        for filename in files:
            if filename.endswith('.json'):
                print(f'{n}/{structure_size}', end='\r')
                file_path = os.path.join(path, filename)
                try:
                    wiki_json = json.load(open(file_path, 'r'))
                except json.JSONDecodeError:
                    print(f'Wrong json format {file_path}')
                    continue
                
                gp_name = wiki_json['GP NAME']
                year = int(wiki_json['YEAR'])

                df_filtered = df[(df['YEAR'] == year) & (df['GP NAME'] == gp_name)]
                wiki_merged = {**wiki_json, 'results': df_filtered.to_dict('records')}
                with open(file_path, 'w') as f:
                    json.dump(wiki_merged, f)