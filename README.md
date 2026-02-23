# ISSessions FantasyCTF 2026

**Team ZeroDays — 2nd Place 🏴‍☠️**  
A 2-day CTF run by ISSessions (Sheridan College's cybersecurity club), themed around medieval fantasy. Challenges spanned crypto, web exploitation, forensics, networking, and programming.

## Files

| File | Challenge | Category | Description |
|------|-----------|----------|-------------|
| `gauntletctf.py` | The Chronomancer's Gauntlet | prog | Live socket solver — auto-parses and solves math, graph, CRT, matrix, knapsack, and LCS problems mid-connection |
| `messagectf.py` | The Goblin Messenger's Cipher | crypto | RSA broadcast attack using Chinese Remainder Theorem (CRT) to recover plaintext from 3 ciphertexts with the same small exponent |
| `jaydenctf.py` | The Hall of Scorching Glyphs | crypto | 4-bit S-box substitution cipher with XOR key decryption |
| `dungeonctf.py` | The Dungeon Cartographer | prog | Dijkstra's algorithm to find minimum cost path through a weighted grid |
| `ctfdragon.py` | Dragon Chat | web | Credential brute-force with rotating CAPTCHA verification answers |
| `equationsctf.py` | Equations | prog | Automated equation solver that loops against a web endpoint until flag is returned |
| `fuzzer.py` | (SQL Injection challenge) | web | Path fuzzer to enumerate hidden endpoints on a target web app |
| `networkingctf.txt` | Silent Messages | networking | Manual TCP flag bit decoding — maps flag combinations to ASCII characters |
| `sniffedctf.txt` | Spell Sequence | forensics | TCP sequence number analysis with Base64-encoded flag extraction |

## Notable

The gauntlet solver (`gauntletctf.py`) was the most involved — it connects over a raw socket and has to identify and solve 5 different problem types dynamically using regex parsing, with no prior knowledge of which problem type comes next.

## Event

- **Organizer:** [ISSessions](https://issessions.ca) — Sheridan College Cybersecurity Club  
- **Sponsors:** KPMG, Trend Micro
- **Teammates:** Nada Elshami, Faith Aikhionbare, and Kai-Ann Parsons  
- **Date:** February 21-22, 2026  
- **Result:** 2nd place out of all competing teams

