from curlit import Request, async

url = "http://127.0.0.1"
NUM = 100

for i in range(NUM):
    curlit.async()
    Request(url, params={"id": i}).perform_async()

url_list = []
