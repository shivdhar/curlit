from io import BytesIO
import json as jsonlib
from urllib.parse import urlencode

import pycurl

from .request import Request
from .response import Response



def get(url, *args, **kwargs):
    method = 'GET'
    return make_request(url, method, *args, **kwargs)


def post(url, *args, **kwargs):
    method = 'POST'
    return make_request(url, method, *args, **kwargs)

def get(url, *args, **kwargs):
    method = 'GET'
    ans = Request(url, method, *args, **kwargs).perform()
    assert isinstance(ans, Response)


def post(url, *args, **kwargs):
    method = 'POST'
    ans = Request(url, method, *args, **kwargs)
    ans = ans.perform()
    assert isinstance(ans, Response)
    return ans