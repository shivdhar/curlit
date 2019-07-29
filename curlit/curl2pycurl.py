import argparse
import logging
import sys
from io import BytesIO

import pycurl
import requests

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def use_pycurl():
    buf = BytesIO()

    curl = pycurl.Curl()

    curl.setopt(pycurl.URL, 'http://127.0.0.1/anything')
    curl.setopt(pycurl.WRITEDATA, buf)
    curl.perform()
    curl.close()

    body = buf.getvalue().decode('iso-8859-1')
    # print(body)


def use_requests():
    resp = requests.get('http://127.0.0.1/anything')
    body = resp.text
    # print(body)


# print('using requests')
# use_requests()
# use_pycurl()


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-X', '--method')
    parser.add_argument('urls', nargs=1)

    return parser


def curl2py(curlstr):
    parser = get_parser()
    args = parser.parse_args(curlstr.strip().lstrip('curl').split())
    log.debug(args)
    if not len(args.urls) == 1:
        raise ValueError
    buf = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, args.urls[0])
    curl.setopt(pycurl.WRITEDATA, buf)
    curl.perform()
    body = buf.getvalue().decode('iso-8859-1')
    log.debug(body)


if __name__ == '__main__':
    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.DEBUG)
    curlstr = 'curl -X GET http://127.0.0.1/json'
    curl2py(curlstr)
