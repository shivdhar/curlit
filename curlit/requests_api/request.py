import json as jsonlib
from io import BytesIO
from urllib.parse import urlencode

import pycurl

from .response import Response


class Request:
    def __init__(self, url,
                 method,
                 params=None,
                 headers=None,
                 files=None,
                 cookies=None,
                 body=None,
                 json=None,
                 encoding='utf-8'):
        self.url = url
        self.method = method
        self.response = None

        self.json = None

        # initialize libcurl easy_handle
        self._handle = pycurl.Curl()
        self._body_buf = BytesIO()
        self._header_buf = BytesIO()

        self.body_raw = None
        self.headers_raw = None

        self._handle.setopt(pycurl.HEADERFUNCTION, self._header_buf.write)
        self._handle.setopt(pycurl.WRITEFUNCTION, self._body_buf.write)

        # set url-encoded url with params, if any, of handle
        if params is None:
            self.full_url = url
        else:
            self.full_url = make_full_url(url, params)
        self._handle.setopt(pycurl.URL, self.url)

        # set headers
        if headers is not None:
            assert isinstance(headers, dict)
            headers = [f'{k}: {v}' for k, v in headers.items()]
            self._handle.setopt(pycurl.HTTPHEADER, headers)

        # set files
        if files is not None:
            assert isinstance(files, dict)
            files = [(k, (pycurl.FORM_FILE, v)) for k, v in files.items()]
            self._handle.setopt(pycurl.HTTPPOST, files)

        # set cookies
        if cookies is not None:
            assert isinstance(cookies, dict)
            cookies = '; '.join((f'{k}={v}' for k, v in cookies.items()))
            self._handle.setopt(pycurl.COOKIE, cookies)

        # set body
        if body is not None:
            body = urlencode(body)
            self._handle.setopt(pycurl.POSTFIELDS, body)

        # set json in body
        if json is not None:
            self._handle.setopt(pycurl.POSTFIELDS, jsonlib.dumps(json).encode(encoding=encoding))
        self._handle.setopt(pycurl.CUSTOMREQUEST, method)

    def perform(self):
        self._handle.perform()
        self.body_raw = self._body_buf.getvalue()
        self.headers_raw = self._header_buf.getvalue()
        return Response(self._handle, self._header_buf, self._body_buf)


def make_full_url(url, params):
    assert isinstance(params, dict)
    full_url = f'{url}?{urlencode(params)}'
    return full_url


def make_request(url,
                 method,
                 params=None,
                 headers=None,
                 files=None,
                 cookies=None,
                 body=None,
                 json=None,
                 encoding='utf-8'):
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

    if json is not None:
        handle.setopt(pycurl.POSTFIELDS, jsonlib.dumps(json).encode(encoding=encoding))
    handle.setopt(pycurl.CUSTOMREQUEST, method)

    handle.perform()

    body = body_buf.getvalue().decode('iso-8859-1')

    return Response(handle, header_buf, body_buf)
