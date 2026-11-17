import os
import json
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

EMBED_MODEL = os.getenv(
    "GEMINI_EMBED_MODEL",
    "gemini-embedding-001"
)

CHAT_MODEL = os.getenv(
    "GEMINI_CHAT_MODEL",
    "gemini-3.5-flash-lite"
)

DIMS = 768


# ===================== JSON PARSING =====================

def parse_json(text):
    if not text or not isinstance(text, str):
        raise ValueError("Gemini returned an empty response")

    text = text.strip()

    # Remove Markdown code fences if present
    text = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        text,
        flags=re.IGNORECASE
    ).strip()

    try:
        result = json.loads(text)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON returned by Gemini: {text[:500]}"
        ) from error

    if not isinstance(result, dict):
        raise ValueError(
            f"Expected JSON object, received {type(result).__name__}"
        )

    return result


# ===================== RETRY HANDLING =====================

def retry_request(func, attempts=2):
    last_error = None

    for attempt in range(attempts):
        try:
            return func()

        except Exception as error:
            last_error = error

            print(
                f"Gemini request failed "
                f"(attempt {attempt + 1}/{attempts}): {error}"
            )

            if attempt < attempts - 1:
                time.sleep(1.5 * (attempt + 1))

    raise RuntimeError(
        f"Gemini request failed after {attempts} attempts: {last_error}"
    )


# ===================== EMBEDDINGS =====================

def embed(text):
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text")

    def request():
        return client.models.embed_content(
            model=EMBED_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=DIMS
            )
        )

    result = retry_request(request)

    if not result.embeddings:
        raise ValueError("Gemini returned no embeddings")

    values = result.embeddings[0].values

    if len(values) != DIMS:
        raise ValueError(
            f"Expected {DIMS} embedding dimensions, "
            f"received {len(values)}"
        )

    return values


# ===================== JSON GENERATION =====================


def generate_json(prompt):
    def request():
        return client.models.generate_content(
            model=CHAT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0
            )
        )

    response = retry_request(request)

    if not response:
        raise ValueError("Gemini returned no response")

    if not response.text:
        finish_reason = (
            response.candidates[0].finish_reason
            if response.candidates
            else "Unknown"
        )

        raise ValueError(
            f"Gemini returned no text. Finish reason: {finish_reason}"
        )


    return parse_json(response.text)
