import requests

base = "https://issessionsctf-sql-injection-challenge.chals.io"

paths = [
    "/admin", "/flag", "/secret", "/hidden",
    "/api", "/api/flag", "/api/secret", "/api/admin",
    "/api/v1", "/api/v1/flag", "/api/v1/secret",
    "/tower", "/archivist", "/archive", "/vault",
    "/door", "/corridor", "/forgotten", "/ruin",
    "/.env", "/config", "/backup", "/debug",
    "/v1", "/v2", "/internal", "/private", "/restricted",
    "/robots.txt", "/sitemap.xml", "/.git/HEAD",
    "/health", "/status", "/info", "/version",
    "/key", "/token", "/data", "/files",
    "/magic", "/void", "/stone",
    "/93", "/00", "/9300", "/93/00",
    "/user", "/users", "/login", "/register",
    "/console", "/shell", "/exec", "/run",
    "/source", "/src", "/code",
    "/note", "/notes", "/memo", "/message",
    "/scroll", "/tome", "/grimoire", "/spell",
]

print(f"Fuzzing {base}...\n")

for path in paths:
    try:
        r = requests.get(base + path, timeout=5, allow_redirects=False)
        if r.status_code != 404:
            print(f"[{r.status_code}] {path}  <-- DIFFERENT! ({len(r.content)} bytes)")
            for k, v in r.headers.items():
                print(f"  Header: {k}: {v}")
            print(f"  Body: {r.text[:500]}")
            print()
        else:
            print(f"[404] {path}")
    except Exception as e:
        print(f"[ERR] {path}: {e}")