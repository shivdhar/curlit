import pycurl
from icecream import ic

from curlit import Request
import json

NUM = int(20e1)

ic = print

url = "http://127.0.0.1/anything"

multi = pycurl.CurlMulti()

bodies = []
for i in range(NUM):
    req = Request(url, "GET", headers={"id": i})
    req._handle.getinfo(pycurl.EFFECTIVE_URL)
    multi.add_handle(req._handle)
    bodies.append(req._body_buf)

ret = 0
while ret != pycurl.E_CALL_MULTI_PERFORM:
    import time

    # time.sleep(1)
    ret, num_left = multi.perform()
    ic(num_left)
    ic(ret, pycurl.E_CALL_MULTI_PERFORM)
    if num_left == 0:
        break
    # if ret != pycurl.E_CALL_MULTI_PERFORM:
    #     break

# num_q, ok_list, err_list = multi.info_read()
# while True:
num_q, ok_list, err_list = multi.info_read()
ic([num_q, ok_list, err_list])
# if num_q == 0:
#     break

assert err_list == [], (len(ok_list), len(err_list))
for body in bodies:
    j = body.getvalue().decode("utf-8")
    s = json.loads(j)
    ic(j)
    # assert isinstance(s, dict)
    # ic(s.keys())
    # ic(s['text'])
    ic(s["headers"]["Id"])

# import pycurl
# c = pycurl.Curl()
# c.setopt(pycurl.URL, "https://curl.haxx.se")
# m = pycurl.CurlMulti()
# m.add_handle(c)
# while 1:
#     ret, num_handles = m.perform()
#     if ret != pycurl.E_CALL_MULTI_PERFORM: break
# while num_handles:
#     ret = m.select(1.0)
#     if ret == -1:  continue
#     while 1:
#         ret, num_handles = m.perform()
#         if ret != pycurl.E_CALL_MULTI_PERFORM: break
