import hashlib
import secrets
import sys

from db import get_conn

if len(sys.argv) < 2:
    raise SystemExit('Usage: python issue_key.py "Company Name"')

name = " ".join(sys.argv[1:])
api_key = secrets.token_urlsafe(24)
key_hash = hashlib.sha256(api_key.encode()).hexdigest()

conn = get_conn()
cur = conn.cursor()
cur.execute(
    "UPDATE agents SET api_key_hash = %s WHERE lower(company_name) = lower(%s) RETURNING company_name",
    (key_hash, name),
)
row = cur.fetchone()
conn.commit()
cur.close()
conn.close()

if not row:
    raise SystemExit(f"No agent named {name}")
print(f"New API key for {row[0]} (shown once, store it now):\n{api_key}")