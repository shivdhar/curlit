import requests

from curlit.requests_api import get


def test_get(_url):
    return get(_url,
               headers={1: 2},
               files={'file': '../setup.py',
                      'file2': __file__},
               cookies={'c1': 1, 'c2': 2}
               )


def test_requests_get(_url):
    return requests.get(_url)


if __name__ == '__main__':
    _url = 'http://127.0.0.1/anything'

    ans = test_get(_url)

    # ans = test_requests_get(_url)

    print(ans)
