import socket
import re
import heapq
from math import gcd
from functools import reduce

HOST = "0.cloud.chals.io"
PORT = 28165

def parse_and_solve(expr):
    tokens = re.findall(r'\d+|[@#*+\-/()]', expr)
    pos = [0]
    def peek(): return tokens[pos[0]] if pos[0] < len(tokens) else None
    def consume():
        t = tokens[pos[0]]; pos[0] += 1; return t
    def parse_expr():
        left = parse_term()
        while peek() in ('+', '-'):
            op = consume(); right = parse_term()
            left = left + right if op == '+' else left - right
        return left
    def parse_term():
        left = parse_xor()
        while peek() == '*':
            consume(); left *= parse_xor()
        return left
    def parse_xor():
        left = parse_pow()
        while peek() == '#':
            consume(); left ^= parse_pow()
        return left
    def parse_pow():
        left = parse_atom()
        while peek() == '@':
            consume(); left = pow(left, parse_atom(), 10007)
        return left
    def parse_atom():
        t = peek()
        if t == '(':
            consume(); val = parse_expr(); consume(); return val
        elif t == '-':
            consume(); return -parse_atom()
        else:
            consume(); return int(t)
    return parse_expr()

def dijkstra(n, edges, src, dst):
    graph = {i: [] for i in range(n)}
    for u, v, w in edges:
        graph[u].append((w, v))
    dist = {i: float('inf') for i in range(n)}
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for w, v in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist[dst]

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def crt(remainders, moduli):
    M = reduce(lambda a, b: a * b, moduli)
    x = 0
    for r, m in zip(remainders, moduli):
        Mi = M // m
        _, inv, _ = extended_gcd(Mi % m, m)
        x += r * Mi * inv
    return x % M

def mod_det(matrix, p):
    n = len(matrix)
    mat = [row[:] for row in matrix]
    det = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if mat[r][col] % p != 0), -1)
        if pivot == -1: return 0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = (-det) % p
        det = (det * mat[col][col]) % p
        inv = pow(mat[col][col], p - 2, p)
        for row in range(col + 1, n):
            factor = (mat[row][col] * inv) % p
            for k in range(col, n):
                mat[row][k] = (mat[row][k] - factor * mat[col][k]) % p
    return det % p

def solve_round(text):
    print(f"\n--- PROBLEM ---\n{text}\n")

    if "EXPRESSION:" in text:
        expr = re.search(r'EXPRESSION:\s*(.+)', text).group(1).strip()
        return str(parse_and_solve(expr))

    if "shortest path" in text.lower() or "CARTOGRAPHY" in text:
        node_match = re.search(r'Nodes:\s*0 to (\d+)', text)
        n = int(node_match.group(1)) + 1 if node_match else 20
        src_dst = re.search(r'from node (\d+) to node (\d+)', text)
        src = int(src_dst.group(1)) if src_dst else 0
        dst = int(src_dst.group(2)) if src_dst else n - 1
        edges = [(int(a), int(b), int(w))
                 for a, b, w in re.findall(r'(\d+)\s*->\s*(\d+)\s*\(weight\s*(\d+)\)', text)]
        return str(dijkstra(n, edges, src, dst))

    if "congruence" in text.lower() or "≡" in text:
        pairs = re.findall(r'x\s*≡\s*(\d+)\s*\(mod\s*(\d+)\)', text)
        if pairs:
            remainders = [int(r) for r, m in pairs]
            moduli = [int(m) for r, m in pairs]
            return str(crt(remainders, moduli))

    if "determinant" in text.lower() or "MATRIX" in text:
        p_match = re.search(r'modulo\s+(\d+)', text)
        p = int(p_match.group(1)) if p_match else 10007
        size_match = re.search(r'(\d+)x(\d+)', text)
        n = int(size_match.group(1)) if size_match else 5
        # Parse matrix between "Matrix:" and "Send"
        matrix_section = text.split("Matrix:")[1].split("Send")[0]
        matrix = []
        for line in matrix_section.strip().split('\n'):
            nums = list(map(int, re.findall(r'\d+', line)))
            if len(nums) == n:
                matrix.append(nums)
        if matrix:
            return str(mod_det(matrix, p))

    if "lcs" in text.lower() or "subsequence" in text.lower():
        seqs = re.findall(r'[A-Z]{4,}', text)
        if len(seqs) >= 2:
            a, b = seqs[0], seqs[1]
            dp = [[0]*(len(b)+1) for _ in range(len(a)+1)]
            for i in range(1, len(a)+1):
                for j in range(1, len(b)+1):
                    dp[i][j] = dp[i-1][j-1]+1 if a[i-1]==b[j-1] else max(dp[i-1][j], dp[i][j-1])
            return str(dp[len(a)][len(b)])

    if "prime" in text.lower():
        match = re.search(r'Is\s+(\d+)\s+prime', text, re.I)
        if match:
            num = int(match.group(1))
            if num < 2: return "NO"
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0: return "NO"
            return "YES"

    if "gcd" in text.lower():
        data_lines = [l for l in text.split('\n') if re.search(r'\d', l)]
        nums = list(map(int, re.findall(r'\d+', data_lines[-1])))
        return str(reduce(gcd, nums))

    if "fibonacci" in text.lower() or "fib" in text.lower():
        data_lines = [l for l in text.split('\n') if re.search(r'\d', l)]
        n = int(re.search(r'\d+', data_lines[-1]).group())
        a, b = 0, 1
        for _ in range(n): a, b = b, a+b
        return str(a)

    # ROUND 5: 0/1 Knapsack
    if "knapsack" in text.lower() or "hoard" in text.lower() or "pack with capacity" in text.lower() or "maximize total value" in text.lower():
        cap_match = re.search(r'capacity\s+(\d+)', text)
        capacity = int(cap_match.group(1))
        items = [(int(w), int(v)) for w, v in re.findall(r'weight=(\d+),\s*value=(\d+)', text)]
        dp = [0] * (capacity + 1)
        for w, v in items:
            for c in range(capacity, w - 1, -1):
                dp[c] = max(dp[c], dp[c - w] + v)
        return str(dp[capacity])

    if "sort" in text.lower():
        data_lines = [l for l in text.split('\n') if re.search(r'\d', l)]
        nums = list(map(int, re.findall(r'-?\d+', data_lines[-1])))
        return " ".join(map(str, sorted(nums)))

    print("[!] Unknown round — paste output so solver can be updated!")
    return "0"

def main():
    import time
    s = socket.socket()
    s.connect((HOST, PORT))
    s.settimeout(8)
    buf = b""

    def recv_until(marker):
        nonlocal buf
        while marker.encode() not in buf:
            try:
                chunk = s.recv(4096)
                if not chunk: break
                buf += chunk
                print(chunk.decode(errors='replace'), end='', flush=True)
            except socket.timeout:
                break
        idx = buf.find(marker.encode()) + len(marker)
        out = buf[:idx].decode(errors='replace')
        buf = buf[idx:]
        return out

    def send(msg):
        s.sendall((msg + "\n").encode())

    recv_until("Select a challenge:")
    send("1")

    for _ in range(5):
        data = recv_until("ANSWER>")
        answer = solve_round(data)
        print(f"\n>>> Sending: {answer}")
        send(answer)
        time.sleep(0.1)

    time.sleep(1)
    try:
        final = s.recv(4096).decode(errors='replace')
        print("\n=== FINAL ===\n", final)
        flag = re.search(r'FantasyCTF\{[^}]+\}', final)
        if flag:
            print(f"\n[+] FLAG: {flag.group(0)}")
    except: pass
    s.close()

if __name__ == "__main__":
    main()