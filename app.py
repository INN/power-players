#!/usr/bin/env python

import json

import argparse
from flask import Flask, render_template

import app_config
from render_utils import smarty_filter, urlencode_filter
import static

from helpers import make_context, state_slug_to_name, get_state_slugs, get_state_data, get_player_slugs, \
    get_player_data, state_name_to_stateface_letter, get_state_slug_name_map, format_currency_filter

app = Flask(__name__)

app.jinja_env.filters['smarty'] = smarty_filter
app.jinja_env.filters['urlencode'] = urlencode_filter

# Power Players filters
app.jinja_env.filters['format_currency'] = format_currency_filter
app.jinja_env.filters['stateface'] = state_name_to_stateface_letter

@app.route('/')
def index():
    """
    Power Players homepage.
    """
    context = make_context()

    with open('data/featured.json') as f:
        context['featured'] = json.load(f)

    context['states'] = get_state_slug_name_map()

    return render_template('index.html', **context)


state_slugs = get_state_slugs()
for slug in state_slugs:
    @app.route('/state/%s/' % slug)
    def state():
        context = make_context()

        from flask import request
        slug = request.path.split('/')[2]

        state = state_slug_to_name(slug)
        context['state'] = {
            'name': state,
            'data': get_state_data(state)
        }

        return render_template('state.html', **context)


player_slugs = get_player_slugs()
for slug in player_slugs:
    @app.route('/player/%s/' % slug)
    def player():
        context = make_context()

        from flask import request
        slug = request.path.split('/')[2]

        player = get_player_data(slug)
        if player:
            context['player'] = player
            return render_template('player.html', **context)
        else:
            return 404


app.register_blueprint(static.static)

# Boilerplate
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    args = parser.parse_args()
    server_port = 8000

    if args.port:
        server_port = int(args.port)

    app.run(host='0.0.0.0', port=server_port, debug=app_config.DEBUG)
