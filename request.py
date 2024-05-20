import requests

url = f"http://localhost:5000"

# ping = requests.get(f'{url}/ping')
# print(ping.text)

def get_stream(url):
    s = requests.Session()
    with s.get(url, headers=None, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
              print("triggered => ")
              yield line.decode('utf-8')

url = f'{url}/generate_stream'
# url = 'https://jsonplaceholder.typicode.com/posts/1'
for line in get_stream(url):
    print(line)