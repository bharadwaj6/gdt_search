"""Utility functions that are used to help search service."""

import copy

from requests_oauthlib import OAuth1

from conf import GOOGLE_CONF, TWITTER_CONF, DUCKDUCKGO_CONF, API_STATUS


def google_request_params(query):
    query_params = copy.deepcopy(GOOGLE_CONF['params'])
    query_params['q'] = query

    args = [GOOGLE_CONF['url']]
    kwargs = {'params': query_params}
    return [args, kwargs]


def twitter_request_params(query):
    query_params = {'q': query}
    auth = OAuth1(
        TWITTER_CONF['params']['app_key'],
        TWITTER_CONF['params']['app_secret'],
        TWITTER_CONF['params']['client_key'],
        TWITTER_CONF['params']['client_secret']
    )

    args = [TWITTER_CONF['url']]
    kwargs = {'params': query_params, 'auth': auth}
    return [args, kwargs]


def duckduckgo_request_params(query):
    query_params = copy.deepcopy(DUCKDUCKGO_CONF['params'])
    query_params['q'] = query

    args = [DUCKDUCKGO_CONF['url']]
    kwargs = {'params': query_params}
    return [args, kwargs]


def clean_async_response(response):
    if response.status_code != 200:
        return {'status': API_STATUS['error'], 'error': 'Request timeout'}
    else:
        return response.json()


def fetch_time_elapsed(resps):
    # duckduckgo doesn't have time taken in its API, so we're using inbuilt time elapsed
    # NOTE: this might not be accurate depending on server load and other things
    # but is good enough since duckduckgo is first request sent in the async pool
    duck_time = resps[0].elapsed.total_seconds()
    if duck_time > 1:
        duck_time = None

    google_response = resps[1].json()
    if 'searchInformation' in google_response:
        google_time = google_response['searchInformation']['searchTime']
    else:
        google_time = None

    twitter_response = resps[2].json()
    if 'search_metadata' in twitter_response:
        twitter_time = twitter_response['search_metadata']['completed_in']
    else:
        twitter_time = None

    return [duck_time, google_time, twitter_time]
