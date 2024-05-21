import requests

url = f"http://localhost:5000"

# ping = requests.get(f'{url}/ping')
# print(ping.text)

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

url = f'{url}/questions/stream-generator'
# url = 'https://jsonplaceholder.typicode.com/posts/1'
for line in get_stream(url):
    print(line)