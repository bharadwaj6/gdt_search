GOOGLE_CONF = {
    'url': 'https://www.googleapis.com/customsearch/v1?',
    'params': {
        'key': '',
        'cx': ''
    }
}

TWITTER_CONF = {
    'url': 'https://api.twitter.com/1.1/search/tweets.json?',
    'params': {
        'app_key': '',
        'app_secret': '',
        'client_key': '',
        'client_secret': ''
    }
}

DUCKDUCKGO_CONF = {
    'url': 'http://api.duckduckgo.com/?',
    'params': {
        'format': 'json'
    }
}

API_STATUS = {
    'success': 200,
    'error': 400
}

REQUEST_TIMEOUT = 1  # 1 second
