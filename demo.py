# import sys

# from db import get_conn
# from routing import publish_post
# from runner import process_pending


# def agent_id_by_name(name):
#     conn = get_conn()
#     cur = conn.cursor()
#     cur.execute("SELECT id FROM agents WHERE lower(company_name) = lower(%s)", (name,))
#     row = cur.fetchone()
#     cur.close()
#     conn.close()
#     if not row:
#         raise SystemExit(f"No agent named {name}")
#     return str(row[0])


# if __name__ == "__main__":
#     author = sys.argv[1] if len(sys.argv) > 1 else "Swiggy"
#     content = " ".join(sys.argv[2:]) or "5% off all deliveries on Diwali."

#     result = publish_post(agent_id_by_name(author), "Update", content)
#     print(f"\n{author} posted: {content}\n")

#     print("NOTIFIED:")
#     for n in result["notified"]:
#         print("  ", n)
#     print("SKIPPED:")
#     for s in result["skipped"]:
#         print("  ", s)

#     print("\nAGENT RESPONSES:")
#     for r in process_pending(result["post_id"]):
#         print("  ", r)


import sys

from db import get_conn
from routing import publish_post
from runner import process_pending


def agent_id_by_name(name):

    conn = get_conn()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT id
            FROM agents
            WHERE lower(company_name) = lower(%s)
              AND is_active = TRUE
        """, (name,))

        row = cur.fetchone()

        if not row:
            raise SystemExit(f"No active agent named {name}")

        return str(row[0])

    finally:

        cur.close()
        conn.close()


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print(
            'Usage: python demo.py Swiggy '
            '"5% off all deliveries on Diwali"'
        )
        sys.exit(1)

    author = sys.argv[1]
    content = " ".join(sys.argv[2:])

    try:

        author_id = agent_id_by_name(author)

        result = publish_post(
            author_id,
            "Update",
            content
        )

        print(f"\n{author} posted: {content}")

        print(f"\nPOST STATUS: {result['status']}")

        if result["status"] == "BLOCKED":

            print("MODERATION:", result["moderation_reason"])
            sys.exit(0)

        print("\nNOTIFIED:")

        for item in result["notified"]:
            print("  ", item)

        print("\nSKIPPED:")

        for item in result["skipped"]:
            print("  ", item)

        print("\nROUTING FAILURES:")

        for item in result["failed"]:
            print("  ", item)

        print("\nAGENT RESPONSES:")

        responses = process_pending(result["post_id"])

        for item in responses:
            print("  ", item)

    except Exception as error:

        print(f"\nERROR: {error}")
        sys.exit(1)