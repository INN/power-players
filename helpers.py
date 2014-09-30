# Helper functions for Power Players project
import app_config
import copytext
import json

from render_utils import flatten_app_config, JavascriptIncluder, CSSIncluder


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


def get_copy():
    return copytext.Copy(app_config.COPY_PATH)
