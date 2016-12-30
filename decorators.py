from functools import wraps

from flask import request, jsonify

from conf import API_STATUS


def fetch_query(view_fn):
    """Check if query has been passed."""

    @wraps(view_fn)
    def decorated_function(*args, **kwargs):
        query = request.args.get('q')
        if query:
            return view_fn()
        else:
            return jsonify({'status': API_STATUS['error'], 'error': 'Pass a query'})
    return decorated_function
