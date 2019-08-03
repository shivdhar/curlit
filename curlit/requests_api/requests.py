from io import BytesIO
from urllib.parse import urlencode

import pycurl

from .response import Response


def make_request(url,
                 method,
                 params=None,
                 headers=None,
                 files=None,
                 cookies=None,
                 body=None):
    body_buf = BytesIO()
    header_buf = BytesIO()
    handle = pycurl.Curl()
    handle.setopt(pycurl.HEADERFUNCTION, header_buf.write)
    handle.setopt(pycurl.WRITEDATA, body_buf)

    if params is not None:
        assert isinstance(params, dict)
        url = f'{url}?{urlencode(params)}'

    handle.setopt(pycurl.URL, url)

    if headers is not None:
        assert isinstance(headers, dict)
        headers = [f'{k}: {v}' for k, v in headers.items()]
        handle.setopt(pycurl.HTTPHEADER, headers)

    if files is not None:
        assert isinstance(files, dict)
        files = [(k, (pycurl.FORM_FILE, v)) for k, v in files.items()]
        handle.setopt(pycurl.HTTPPOST, files)

    if cookies is not None:
        assert isinstance(cookies, dict)
        cookies = '; '.join((f'{k}={v}' for k, v in cookies.items()))
        handle.setopt(pycurl.COOKIE, cookies)

    if body is not None:
        body = urlencode(body)
        handle.setopt(pycurl.POSTFIELDS, body)

    handle.setopt(pycurl.CUSTOMREQUEST, method)

    handle.perform()

    body = body_buf.getvalue().decode('iso-8859-1')

    return Response(handle, header_buf, body_buf)


def get(url, *args, **kwargs):
    method = 'GET'
    return make_request(url, method, *args, **kwargs)


def post(url, *args, **kwargs):
    method = 'POST'
    return make_request(url, method, *args, **kwargs)
