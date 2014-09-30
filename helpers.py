# Helper functions for Power Players project
import app_config
import copytext
import json
import re

from render_utils import flatten_app_config, JavascriptIncluder, CSSIncluder
from unicodedata import normalize

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def get_state_names(copy=None):
    not_states = ['content', ] # Spreadsheet sheet names that are not state names
    if copy:
        return [state for state in json.loads(copy.json()).keys() if state not in not_states]
    else:
        return None


def get_state_slugs():
    states = get_state_names(get_copy())
    return [state.lower().replace(' ', '-') for state in states]


def get_state_data(name=None):
    copy = get_copy()
    return copy[name]


def state_slug_to_name(slug):
    copy = get_copy()
    states = get_state_names(copy)
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
    states = get_state_names(copy)
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

