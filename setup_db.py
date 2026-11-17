import sys

from db import get_conn


def drop_all_tables(cur):
    cur.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
    )
    tables = [row[0] for row in cur.fetchall()]
    for t in tables:
        cur.execute(f'DROP TABLE IF EXISTS "{t}" CASCADE')
    print("Dropped tables:", tables)


def main():
    with get_conn() as conn:
        cur = conn.cursor()

        if "--reset" in sys.argv:
            confirm = input(
                "This deletes ALL agents, posts and comments. Type yes to continue: "
            )
            if confirm.strip().lower() != "yes":
                print("Cancelled.")
                return
            drop_all_tables(cur)

        with open("schema.sql", "r", encoding="utf-8") as f:
            cur.execute(f.read())

        cur.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public' ORDER BY table_name"
        )
        print("Tables in database:", [row[0] for row in cur.fetchall()])


if __name__ == "__main__":
    main()