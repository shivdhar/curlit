from .request import Request


def get(url, **kwargs):
    return _make_request(url, method="GET", **kwargs)


def post(url, **kwargs):
    return _make_request(url, method="POST", **kwargs)


def _make_request(url, method, **kwargs):
    try:
        debug = kwargs.pop("debug")
    except KeyError:
        debug = False

    return Request(url, method=method, **kwargs).perform(debug=debug)
