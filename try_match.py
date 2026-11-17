import sys
from db import get_conn
from llm import embed

post = " ".join(sys.argv[1:]) or "5% off all deliveries on Diwali."
vec = embed(post)

conn = get_conn()
cur = conn.cursor()
cur.execute(
    """
    SELECT company_name, interest_embedding <=> %s::vector AS distance
    FROM agents
    ORDER BY distance
    """,
    (str(vec),),
)
print(f"Post: {post}\n")
for name, distance in cur.fetchall():
    print(f"{name:12s} distance {distance:.3f}")
cur.close()
conn.close()