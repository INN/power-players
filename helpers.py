# Helper functions for Power Players project
import app_config
import copytext
import json
import re

from render_utils import flatten_app_config, JavascriptIncluder, CSSIncluder
from unicodedata import normalize

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def get_state_names():
    copy = get_copy()
    not_states = ['content', ] # Spreadsheet sheet names that are not state names
    ret = [state for state in json.loads(copy.json()).keys() if state not in not_states]
    ret.sort()
    return ret


def get_state_slugs():
    states = get_state_names()
    ret = [state.lower().replace(' ', '-') for state in states]
    ret.sort()
    return ret


def get_state_slug_name_map():
    return dict(zip(get_state_slugs(), get_state_names()))


def get_state_data(name=None):
    copy = get_copy()
    return copy[name]


def state_slug_to_name(slug):
    copy = get_copy()
    states = get_state_names()
    for state in states:
        if state.lower() == slug.replace('-', ' '):
            return state


def get_player_data(name):
    data = get_players_data()
    try:
        return data[slugify(unicode(name))]
    except KeyError:
        return None


def get_players_data():
    data = {}
    copy = get_copy()
    states = get_state_names()
    for state in states:
        for row in copy[state]:
            slug = slugify(row['Donor name'])
            data[slug] = {column: row[column] for column in row._columns}
    return data


def get_player_slugs():
    data = get_players_data()
    return data.keys()


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def get_copy():
    return copytext.Copy(app_config.COPY_PATH)


def state_name_to_stateface_letter(name):
    state_map = {
        'Alabama': 'B',
        'Alaska': 'A',
        'Arizona': 'D',
        'Arkansas': 'C',
        'California': 'E',
        'Colorado': 'F',
        'Connecticut': 'G',
        'Delaware': 'H',
        'Florida': 'I',
        'Georgia': 'J',
        'Hawaii': 'K',
        'Idaho': 'M',
        'Illinois': 'N',
        'Indiana': 'O',
        'Iowa': 'L',
        'Kansas': 'P',
        'Kentucky': 'Q',
        'Louisiana': 'R',
        'Maine': 'U',
        'Maryland': 'T',
        'Massachusetts': 'S',
        'Michigan': 'V',
        'Minnesota': 'W',
        'Mississippi': 'Y',
        'Missouri': 'X',
        'Montana': 'Z',
        'Nebraska': 'c',
        'Nevada': 'g',
        'New Hampshire': 'd',
        'New Jersey': 'e',
        'New Mexico': 'f',
        'New York': 'h',
        'North Carolina': 'a',
        'North Dakota': 'b',
        'Ohio': 'i',
        'Oklahoma': 'j',
        'Oregon': 'k',
        'Pennsylvania': 'l',
        'Rhode Island': 'm',
        'South Carolina': 'n',
        'South Dakota': 'o',
        'Tennessee': 'p',
        'Texas': 'q',
        'Utah': 'r',
        'Vermont': 't',
        'Virginia': 's',
        'Washington': 'u',
        'West Virginia': 'w',
        'Wisconsin': 'v',
        'Wyoming': 'x',
    }
    return state_map.get(name, None)
