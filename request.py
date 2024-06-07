import requests
from config import PORT

# URL = f"http://localhost:{PORT}"
URL = f"http://localhost:5000"
# URL = f"http://20.80.233.67:{PORT}"

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

    url = f'{URL}/questions/topic'
    # url = 'https://jsonplaceholder.typicode.com/posts/1'
    data_rcv = ''
    for line in get_stream(url):
        data_rcv += line[6:]
        print(f"{data_rcv}\n")

def post_questions(question, is_bahasa=True):
    payload = {
        'id': "1",
        'question': question,
        'isBahasa': is_bahasa
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

    url = f'{URL}/questions/topic'
    # url = 'https://jsonplaceholder.typicode.com/posts/1'
    data_rcv = ''
    for line in get_stream(url):
        # print(line)
        data_rcv += line[6:]
        print(f"{data_rcv}\n")

# get_ping()
# post_stream_generator()
# post_questions("bagaimana Pengambilan MK non-Konversi di semester yang sama dengan pengambilan MK Konversi? jawab bahasa indonesia")
# post_questions("who are you?", is_bahasa=False)
# post_questions("tell me By participating in the MSIB program at Gojek for the past 4.5 months,?", is_bahasa=False)
# post_questions("what FBON service is?", is_bahasa=False)
# post_questions("Weekly Tracker Automation?", is_bahasa=False)
# post_questions("tell me Weekly Summary September 22, 2023", is_bahasa=False)
# post_questions("please tell me about UUD 1945 pasal 11?", is_bahasa=True)
# post_questions("please tell me about pasal 11?", is_bahasa=False)
# post_questions("apa isi UUD 1945 pasal 11?", is_bahasa=True)
# post_questions("What he did During the week of August 28?", is_bahasa=False)
# post_questions("could you tell me about FBON project?", is_bahasa=False)
# post_questions("tell me about ITS Surabaya", is_bahasa=False)
# post_questions("what is the requirement to follow internship program", is_bahasa=False)
# post_questions("jelaskan mengenai pertukaran pelajar", is_bahasa=True)
# post_questions("apa tujuan dari pertukaran pelajar?", is_bahasa=True)
# post_questions("jelaskan mekanisme dari pertukaran pelajar", is_bahasa=True)
# post_questions("Apa itu ITS?", is_bahasa=True)
# post_questions("sebutkan 5 proyek Ditjen Diktiristek?", is_bahasa=True)
# post_questions("jelaskan Peraturan Menteri Pendidikan dan Kebudayaan Nomor 45 Tahun 2019?", is_bahasa=True)
# post_questions("apa visi dan misi Direktor Jenderal Pendidikan Tinggi, Riset, dan Teknologi?", is_bahasa=True)
# post_questions("siapa saja Keanggotaan Tim dalam pengerjaan proyek?", is_bahasa=True)
# post_questions("Apa itu Kerja Praktik?", is_bahasa=True)
# post_questions("Bagaimana SOP KP?", is_bahasa=True)
# post_questions("hi, siapa anda?", is_bahasa=True)
# post_questions("apa isi dari UUD 1945?", is_bahasa=True)
# post_questions("siapakah rektor ITS 2022?", is_bahasa=True)
post_questions("dimanakah jakarta?", is_bahasa=True)


