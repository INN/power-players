# Helper functions for Power Players project
import app_config
import copytext
import json
import re

from flask import url_for
from render_utils import flatten_app_config, JavascriptIncluder, CSSIncluder
from project_copy import PlayersCopy
from unicodedata import normalize
from werkzeug.routing import BuildError

CACHE = {}

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

EXCLUDED_STATES = [
    'Vermont',
    'Louisiana',
    'Pennsylvania',
    'Maine',
    'Montana',
    'New York'
]

# State data
def get_state_names():
    copy = get_copy()
    # Spreadsheet sheet names that are not state names or states that have been excluded
    not_states = ['content', 'By Location', ] + EXCLUDED_STATES
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
    ret = []
    for row in copy[name]:
        ret.append(row)
    return ret


def state_slug_to_name(slug):
    copy = get_copy()
    states = get_state_names()
    for state in states:
        if state.lower() == slug.replace('-', ' '):
            return state


def get_state_contrib_allocations(state):
    copy = get_copy()
    ret = {}
    for row in copy['By Location']:
        if row['State'] == state:
            slug = slugify(row['Powerplayer'])
            tmp = {}
            for column in row.__dict__['_columns']:
                if column != 'Powerplayer':
                    tmp[column] = row[column]
            ret[slug] = tmp
    return ret


def get_player_contrib_allocations(name):
    slug = slugify(name)
    state = get_player_state(name)
    data = get_state_contrib_allocations(state)
    try:
        return { slugify(name): data[slug] }
    except KeyError:
        return None


# Individual donors/players
def get_player_data(name):
    data = get_players_data()
    try:
        ret = data[slugify(unicode(name))]
        ret['location_data'] = json.dumps(get_player_contrib_allocations(name))
        return ret
    except KeyError:
        return None


def get_player_state(name):
    copy = get_copy()
    states = get_state_names()
    for state in states:
        for row in copy[state]:
            if row['Donor Name'] == name or slugify(row['Donor Name']) == name:
                return state
    return None


def get_players_data():
    data = {}
    copy = get_copy()
    states = get_state_names()
    for state in states:
        for row in copy[state]:
            slug = slugify(row['Donor Name'])
            data[slug] = {column: row[column] for column in row._columns}
    return data


def get_player_slugs():
    data = get_players_data()
    return data.keys()


# Other helpers
def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def get_copy():
    if not CACHE.get('copy', None):
        CACHE['copy'] = PlayersCopy(app_config.COPY_PATH)
    return CACHE['copy']


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


def format_currency_filter(value):
    try:
        return "${:,.2f}".format(float(value))
    except:
        return None


def make_context(asset_depth=0):
    """
    Create a base-context for rendering views.
    Includes app_config and JS/CSS includers.

    `asset_depth` indicates how far into the url hierarchy
    the assets are hosted. If 0, then they are at the root.
    If 1 then at /foo/, etc.
    """
    context = flatten_app_config()

    context['COPY'] = PlayersCopy(app_config.COPY_PATH)
    context['JS'] = JavascriptIncluder(asset_depth=asset_depth)
    context['CSS'] = CSSIncluder(asset_depth=asset_depth)

    return context


def project_url_for(endpoint, **values):
    target = app_config.DEPLOYMENT_TARGET
    targets = ['staging', 'production', ]
    filename = values.get('filename', None)
    project_slug = app_config.PROJECT_SLUG

    # URL for assets dir
    if endpoint is 'assets' and filename is not None:
        if target not in targets:
            return '/assets/' + filename
        else:
            return '/' + project_slug + '/assets/' + filename

    # URL for routes defined in app.py
    try:
        if target not in targets:
            return url_for(endpoint, **values)
        else:
            return "/" + project_slug + url_for(endpoint, **values)
    except BuildError:
        if endpoint is 'home':
            if target not in targets:
                return '/'
            else:
                return '/' + project_slug + '/'
        else:
            raise
