from .pylucene_indexer import search_for_drivers, search_bad_weather, find_controversies
from .queries import find_wins, find_dnfs, join_controversy_context
# {'2005-italian-grand-prix': {'Fernando Alonso': 2, 'Mark Webber': 14}, '2005-turkish-grand-prix': {'Fernando Alonso': 2, 'Mark Webber': 'DNF'}, '2005-belgian-grand-prix': {'Fernando Alonso': 2, 'Mark Webber': 4}, '2005-australian-grand-prix': {'Fernando Alonso': 3, 'Mark Webber': 5}, '2005-spanish-grand-prix': {'Fernando Alonso': 2, 'Mark Webber': 6}, '2005-british-grand-prix': {'Fernando Alonso': 2, 'Mark Webber': 11}, '2005-bahrain-grand-prix': {'Fernando Alonso': 1, 'Mark Webber': 6}, '2005-hungarian-grand-prix': {'Fernando Alonso': 11, 'Mark Webber': 7}, '2005-european-grand-prix': {'Fernando Alonso': 1, 'Mark Webber': 'DNF'}, '2005-french-grand-prix': {'Fernando Alonso': 1, 'Mark Webber': 12}}
def test_query1():
    name1 = 'Fernando Alonso'
    name2 = 'Mark Webber'
    year = '2005'
    gp = '2005-italian-grand-prix'
    print(50*'-')
    print(f'Test 1\n{name1}|{name2}|{year}: ')
    files = search_for_drivers(name1, name2, year)
    wins_dict = find_wins(name1, name2, files)
    if wins_dict is None:
        print('FAILED (no results found)')
    elif wins_dict.get(gp, None) == {'Fernando Alonso': 2, 'Mark Webber': 14}:
        print('PASSED')
    else:
        print(f'FAILED ({gp} not found)')

# {'2004-malaysian-grand-prix': 4, '2004-british-grand-prix': 4, '2005-hungarian-grand-prix': 6, '2005-french-grand-prix': 5, '2005-german-grand-prix': 'NA', '2005-brazilian-grand-prix': 5, '2004-san-marino-grand-prix': 4, '2004-hungarian-grand-prix': 5, '2004-australian-grand-prix': 6}
def test_query2():
    years = '2004 2005'
    weather = 'rain'
    gp = '2004-malaysian-grand-prix'
    print(50*'-')
    print(f'Test 2\n{years}|{weather}: ')
    files = search_bad_weather(weather, years)
    dnfs_dict = find_dnfs(files, 3)
    if dnfs_dict is None:
        print('FAILED (no results found)')
    elif dnfs_dict.get(gp, None) == 4:
        print('PASSED')
    else:
        print(f'FAILED ({gp} not found)')

# {'2005-united-states-grand-prix': {'context': '... ort – Tyre controversy leaves For ...'}, '2004-belgian-grand-prix': {'context': '... ry was the controversy surroundin ...', 'drivers': {'#6 Kimi Räikkönen': 1, '#1 Michael Schumacher': 2, '#2 Rubens Barrichello': 3}}}
def test_query3():
    years = '2004 2005'
    gp = '2004-belgian-grand-prix'
    print(50*'-')
    print(f'Test 3\n{years}: ')
    files = find_controversies(years)
    result_dict = join_controversy_context(files)
    expected_result = {'#6 Kimi Räikkönen': 1, '#1 Michael Schumacher': 2, '#2 Rubens Barrichello': 3}
    if result_dict is None:
        print('FAILED (no results found)')
        return
    elif result_dict.get(gp).get('drivers') == expected_result:
        print('PASSED')
    else:
        print(f'FAILED ({gp} not found)')