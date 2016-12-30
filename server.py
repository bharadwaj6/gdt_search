"""Flask app which acts as a meta search engine service."""

from flask import Flask
from flask import request, jsonify
import requests
import grequests


from conf import REQUEST_TIMEOUT, API_STATUS
from decorators import fetch_query
from utils import twitter_request_params, google_request_params, duckduckgo_request_params
from utils import clean_async_response, fetch_time_elapsed

app = Flask(__name__)


@app.route('/duckduckgo/')
@fetch_query
def search_duckduckgo():
    """Search duckduckgo."""
    query = request.args.get('q')
    args, kwargs = duckduckgo_request_params(query)

    resp = requests.get(*args, **kwargs)
    final_response = {
        '_status': API_STATUS['success']
    }
    final_response['results'] = resp.json()
    return jsonify(final_response)


@app.route('/google/')
@fetch_query
def search_google():
    """Search google."""
    query = request.args.get('q')
    args, kwargs = google_request_params(query)

    resp = requests.get(*args, **kwargs)
    final_response = {
        '_status': API_STATUS['success']
    }
    final_response['results'] = resp.json()['items']
    return jsonify(**final_response)


@app.route('/twitter/')
@fetch_query
def search_twitter():
    """Search twitter."""
    query = request.args.get('q')
    args, kwargs = twitter_request_params(query)

    resp = requests.get(*args, **kwargs)
    final_response = {
        '_status': API_STATUS['success']
    }
    final_response['results'] = resp.json()['statuses']
    return jsonify(**final_response)


@app.route('/_all/')
@fetch_query
def search_all():
    """To search all three resources.

    Using grequests to make asynchronous requests to different search engines.
    """
    query = request.args.get('q')
    dargs, dkwargs = duckduckgo_request_params(query)
    gargs, gkwargs = google_request_params(query)
    targs, tkwargs = twitter_request_params(query)

    reqs = [
        grequests.get(*dargs, timeout=REQUEST_TIMEOUT, **dkwargs),
        grequests.get(*gargs, timeout=REQUEST_TIMEOUT, **gkwargs),
        grequests.get(*targs, timeout=REQUEST_TIMEOUT, **tkwargs)
    ]

    resps = grequests.map(reqs)
    response_times = fetch_time_elapsed(resps)
    query_time = max(response_times)
    # no of services that failed to respond in the given time
    search_fails = sum([1 for x in response_times if x is None])

    final_response = {
        '_time_taken': query_time,
        '_search_fails': search_fails,
        '_status': API_STATUS['success'],
        'duckduckgo': clean_async_response(resps[0]),
        'google': clean_async_response(resps[1]),
        'twitter': clean_async_response(resps[2])
    }
    return jsonify(**final_response)


if __name__ == "__main__":
    app.run(threaded=True)
