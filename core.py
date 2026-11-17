import hashlib
import secrets

from db import get_conn
from llm import embed


def register_agent(
    company_name,
    industry_category,
    interest_manifesto,
    offers_text="",
    excludes_text="",
    aliases=None
):
    """Register or update a company agent."""

    aliases = aliases or []

    # Generate interest embedding
    vector = embed(
        f"{company_name}. {industry_category}. {interest_manifesto}"
    )

    api_key = secrets.token_urlsafe(24)
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO agents (
                company_name,
                industry_category,
                interest_manifesto,
                offers_text,
                excludes_text,
                interest_embedding,
                api_key_hash,
                aliases
            )
            VALUES (
                %s, %s, %s, %s, %s, %s::vector, %s, %s
            )
            ON CONFLICT (company_name) DO UPDATE SET
                industry_category = EXCLUDED.industry_category,
                interest_manifesto = EXCLUDED.interest_manifesto,
                offers_text = EXCLUDED.offers_text,
                excludes_text = EXCLUDED.excludes_text,
                interest_embedding = EXCLUDED.interest_embedding,
                api_key_hash = EXCLUDED.api_key_hash,
                aliases = EXCLUDED.aliases
            RETURNING id
            """,
            (
                company_name,
                industry_category,
                interest_manifesto,
                offers_text,
                excludes_text,
                str(vector),
                key_hash,
                aliases
            ),
        )

        agent_id = cur.fetchone()[0]
        conn.commit()

        return agent_id, api_key

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
