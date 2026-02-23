import requests
import re
from bs4 import BeautifulSoup

url = "https://issessionsctf-equations.chals.io/equations/challenge"

session = requests.Session()

while True:
    r = session.get(url)
    text = r.text

    soup = BeautifulSoup(text, "html.parser")
    data = soup.find("p", class_="data")
    
    if not data:
        print("No equation found. Full response:")
        print(text)
        break

    equation = data.text.strip()
    print(f"Equation: {equation}")

    try:
        answer = int(eval(equation))
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"Error solving '{equation}': {e}")
        break

    r2 = session.get(url, params={"answer": answer})
    print(f"Submitted. Status: {r2.status_code}")

    if "FantasyCTF" in r2.text:
        flag = re.search(r'FantasyCTF\{[^}]+\}', r2.text)
        print(f"\n[+] FLAG: {flag.group(0) if flag else r2.text}")
        break

    soup2 = BeautifulSoup(r2.text, "html.parser")
    if not soup2.find("p", class_="data"):
        print("No more equations. Final response:")
        print(r2.text)
        break