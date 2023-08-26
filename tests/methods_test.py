import requests

from curlit.requests_api import get


def test_get():
    _url = "https://httpbin.org/anything"
    kwargs = {
        "headers": {"1": "2"},
        #    "files":{'file': '../pyproject.toml',
        #           'file2': __file__},
        #    "cookies":{'c1': "1", 'c2': "2"}
    }
    requests_get = requests.get(_url, **kwargs)
    curlit_get = get(_url, debug=True, **kwargs)
    print(curlit_get, requests_get)
    # assert curlit_get == requests_get
