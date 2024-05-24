import requests
from config import PORT

URL = f"http://localhost:{PORT}"

def get_ping():
    ping = requests.get(f'{URL}/ping')
    print(ping.text)

def post_stream_generator():
    payload = {
        'id': "1",
        'question': 'hello world'
    }

    headers = {
        'Content-Type': 'application/json'
    }

    def get_stream(url):
        s = requests.Session()
        with s.post(url, headers=headers, json=payload, stream=True) as resp:
        # with s.post(url, headers={'Content-Type': 'application/json'}, stream=True) as resp:
            for line in resp.iter_lines():
                if line:
                    print("triggered => ")
                    yield line.decode('utf-8')

    url = f'{URL}/questions/stream-generator'
    # url = 'https://jsonplaceholder.typicode.com/posts/1'
    data_rcv = ''
    for line in get_stream(url):
        data_rcv += line[6:]
        print(f"{data_rcv}\n")

def post_questions(question, is_bahasa=True):
    payload = {
        'id': "1",
        'question': question,
        'is_bahasa': is_bahasa
    }

    headers = {
        'Content-Type': 'application/json'
    }

    def get_stream(url):
        s = requests.Session()
        with s.post(url, headers=headers, json=payload, stream=True) as resp:
        # with s.post(url, headers={'Content-Type': 'application/json'}, stream=True) as resp:
            for line in resp.iter_lines():
                if line:
                    print("triggered => ")
                    yield line.decode('utf-8')

    url = f'{URL}/questions'
    # url = 'https://jsonplaceholder.typicode.com/posts/1'
    data_rcv = ''
    for line in get_stream(url):
        data_rcv += line[6:]
        print(f"{data_rcv}\n")

# get_ping()
# post_stream_generator()
# post_questions("bagaimana Pengambilan MK non-Konversi di semester yang sama dengan pengambilan MK Konversi? jawab bahasa indonesia")
# post_questions("who are you?", is_bahasa=False)
post_questions("who are you?", is_bahasa=True)
