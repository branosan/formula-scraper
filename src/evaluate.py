from . import *

f1_2004_2005 = {
    '2004': [
        "australian-grand-prix",
        "malaysian-grand-prix",
        "bahrain-grand-prix",
        "san-marino-grand-prix",
        "spanish-grand-prix",
        "monaco-grand-prix",
        "european-grand-prix",
        "canadian-grand-prix",
        "united-states-grand-prix",
        "french-grand-prix",
        "british-grand-prix",
        "german-grand-prix",
        "hungarian-grand-prix",
        "belgian-grand-prix",
        "italian-grand-prix",
        "chinese-grand-prix",
        "japanese-grand-prix",
        "brazilian-grand-prix"
    ],
    '2005': [
        "australian-grand-prix",
        "malaysian-grand-prix",
        "bahrain-grand-prix",
        "san-marino-grand-prix",
        "spanish-grand-prix",
        "monaco-grand-prix",
        "european-grand-prix",
        "canadian-grand-prix",
        "united-states-grand-prix",
        "french-grand-prix",
        "british-grand-prix",
        "german-grand-prix",
        "hungarian-grand-prix",
        "turkish-grand-prix",
        "italian-grand-prix",
        "belgian-grand-prix",
        "brazilian-grand-prix",
        "japanese-grand-prix",
        "chinese-grand-prix"
    ]
}

def evaluate(data):
    """
    Returns a tuple with tp, fp, and fn values
    """
    tp = 0
    fp = 0
    fn = 0

    for year, races in f1_2004_2005.items():
        for race in races:
            race_key = f'{year}-{race}'
            if race_key in data:
                tp += 1
            else:
                fn += 1

    for gp_name in data:
        year = gp_name.split('-')[0]
        name = '-'.join(gp_name.split('-')[1:])
        if name not in f1_2004_2005[year]:
            fp += 1

    return tp, fp, fn