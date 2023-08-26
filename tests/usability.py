import curlit
from icecream import ic

url = "http://127.0.0.1/anything"

# response = curlit.get(url, params={'sudgsid': 'oiwefowefw'})
# ic(response.__dict__)
# response = curlit.post(url, params={'sudgsid': 'oiwefowefw'},
#                    files={'b': 'usability.py'},
#                    cookies={'a': 'b', 'time-remaining': 100})
# ic(response.__dict__)
oldresp = curlit.post(url, params={"sudgsid": "oiwefowefw"}, json={"a": 7})
response = curlit.Request(
    url, "POST", params={"sudgsid": "oiwefowefw"}, json={"a": 7}
).perform()

ic(response)
ic(response.__dict__)
ic(oldresp.__dict__)
assert oldresp == response
