import json as jsonlib
import pycurl

info_fields = {
    'effective_url': pycurl.EFFECTIVE_URL,
    'response_code': pycurl.RESPONSE_CODE,
    'http_connectcode': pycurl.HTTP_CONNECTCODE,
    'http_version': pycurl.INFO_HTTP_VERSION,
}


class Response:
    def __init__(self, handle, header_buf, body_buf):
        self.handle = handle
        self._header_buf = header_buf
        self.headers = self._make_headers_dict()
        self.body = body_buf.getvalue()

        self.info = self._make_info()
        self.status = self.info['response_code']

        self.ok = False
        if self.status in range(200, 300):
            self.ok = True

        self.text = None
        try:
            self.text = self.body.decode()
        except UnicodeDecodeError:
            pass

        self.json = None
        try:
            self.json = jsonlib.loads(self.text)
        except jsonlib.JSONDecodeError:
            pass

    def _make_headers_dict(self):
        header_str = self._header_buf.getvalue().decode('utf-8')
        from icecream import ic
        ic(header_str)
        header_list = header_str.strip().splitlines()
        headers = {}
        for i, line in enumerate(header_list):
            if i == 0 and line.startswith('HTTP'):
                continue
            k, v = line.split(':', maxsplit=1)
            k = k.strip()
            v = v.strip()
            headers[k] = v
        return headers

    def _make_info(self):
        handle = self.handle
        info_dict = {}
        for k, v in info_fields.items():
            info_dict[k] = handle.getinfo(v)
        return info_dict
