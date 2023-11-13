from . import *

def find_wins(p1, p2, files):
    df = pd.read_csv('data/procesed_data/df_entities.csv', sep=';')
    # results = [f'{p1.title()} and {p2.title()} met during:']
    results = {}
    for file_path in files:
        if re.search(r'(\d{4} .+ [Gg]rand [Pp]rix)', file_path) is None:
            continue
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            year = json_data['title'].split(' ')[0]
            gp_name = '-'.join(json_data['title'].split(' ')[1:]).lower()

            filtered_p1 = df[(df['DRIVER NAME'].str.contains(p1, case=False)) & (df['YEAR'] == int(year)) & (df['GP NAME']==gp_name)]
            filtered_p2 = df[(df['DRIVER NAME'].str.contains(p2, case=False)) & (df['YEAR'] == int(year)) & (df['GP NAME']==gp_name)]
            pairs = filtered_p1.merge(filtered_p2, on=['YEAR', 'GP NAME'])
            
            if pairs.shape[0] == 0:
                continue
            # check if both pilots finished the race
            pos_x = 'DNF' if pairs['POS_x'][0] < 0 else pairs['POS_x'][0]
            pos_y = 'DNF' if pairs['POS_y'][0] < 0 else pairs['POS_y'][0]
            # add print statement to results
            results[f'{year}-{gp_name}'] = {p1.title(): pos_x, p2.title(): pos_y}
    return results

def find_dnfs(files, year_range):
    df = pd.read_csv('data/procesed_data/df_entities.csv', sep=';')
    # remap string values to int
    results = {}
    for file_path in files:
        if re.search(r'(\d{4} .+ [Gg]rand [Pp]rix)', file_path) is None:
            continue
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            year = int(json_data['title'].split(' ')[0])
            gp_name = '-'.join(json_data['title'].split(' ')[1:]).lower()

            filtered = df[
                (df['YEAR'] == year) & 
                (df['GP NAME'] == gp_name)
            ]
            filtered = filtered[filtered['POS'] < 0]
            if filtered.shape[0] == 0:
                continue
            results[f'{year}-{gp_name}'] = filtered.shape[0]
    return results

# !!!!
# Deprecated queries which wont be used in the final version
# !!!!

def find_pairs(p1, p2, year):
    """
    Returns a dataframe of grand prix in which both pilot1 and pilot2 were driving
    """
    df = pd.read_csv('procesed_data/df_entities.csv', sep=';')

    filtered_p1 = df[df['DRIVER NAME'].str.contains(p1, case=False)]
    filtered_p2 = df[df['DRIVER NAME'].str.contains(p2, case=False)]
    
    filtered_p1 = filtered_p1[filtered_p1['YEAR'] == year]
    filtered_p2 = filtered_p2[filtered_p2['YEAR'] == year]

    pairs = filtered_p1.merge(filtered_p2, on=['YEAR', 'GP NAME'])
    return pairs[['YEAR', 'GP NAME']].head()

def find_entity_wiki(name):
    url = 'https://en.wikipedia.org/wiki/'
    path = url + '_'.join(name.split(' ')[1:]).title()
    page = None
    try:
        with open(f'data/{path}/page.txt', 'r') as f:
            page = f.read()
    except FileNotFoundError:
        print('Wrong path or file does not exist')
        return None
    wins_reges = r'[wW]ins(\d+)'
    wins = re.findall(wins_reges, page)
    if len(wins) == 0:
        return None
    return wins[0]

def find_most_wins(gp_name, group_by_tag='DRIVER NAME'):
    """
    Returns a dataframe of drivers with most wins in a given grand prix and their total number of wins
    """
    df = pd.read_csv('procesed_data/df_entities.csv', sep=';')
    filtered = None
    try:
        filtered = df[(df['GP NAME'].str.contains(gp_name, case=False)) & (df['POS'] == 1)]
        filtered = filtered.groupby([group_by_tag]).size().reset_index(name='counts')
        filtered = filtered.sort_values(by=['counts'], ascending=False)
        # filtered.iloc[0, 0]
        # x == row
        # y == column
        filtered['WINS'] = filtered['DRIVER NAME'].apply(find_entity_wiki)
        return filtered.head()
    except KeyError:
        print('Wrong group_by_tag provided')
        return 'No drivers found'
    
def find_collegues(p1, p2):
    """
    Returns a list of years and team names in which both pilot1 and pilot2 were driving for the same team
    """
    df = pd.read_csv('procesed_data/df_entities.csv', sep=';')
    filtered_p1 = df[df['DRIVER NAME'].str.contains(p1, case=False)]
    filtered_p2 = df[df['DRIVER NAME'].str.contains(p2, case=False)]

    pairs = filtered_p1.merge(filtered_p2, on=['YEAR', 'TEAM NAME'])
    return pairs.drop_duplicates(subset=['YEAR', 'TEAM NAME'])[['YEAR', 'TEAM NAME']].sort_values(by=['YEAR'])