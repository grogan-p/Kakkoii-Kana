import random
import time
import requests  # type: ignore[import-untyped]

from kana import UnknownKana, romanizations

API = "https://jisho.org/api/v1/search/words"
HEADERS = {"User-Agent": "KakkoiiKana/0.1 (personal learning project)"}
PAGE_DELAY = 0.5

_pool: list[dict[str, object]] = []


def _is_hiragana(text: str) -> bool:
    return bool(text) and all(0x3041 <= ord(c) <= 0x3096 for c in text)


def make_question(kana: str, kanji: str | None, meaning: list[str]) -> dict:
    """Bundle a word with its accepted romaji. Raises UnknownKana if ungradeable."""
    accepted = sorted(romanizations(kana))
    return {"kana": kana, "kanji": kanji, "meaning": meaning, "accepted": accepted}


def _to_question(entry: dict) -> dict | None:
    """Convert a Jisho entry to a question, or None if we can't use it."""
    if not entry.get("is_common"):
        return None
    try:
        jp = entry["japanese"][0]
        reading = jp.get("reading") or jp.get("word", "")
        if not _is_hiragana(reading):
            return None
        meaning = entry["senses"][0]["english_definitions"][:3]
        kanji = jp.get("word") if jp.get("reading") else None
        return make_question(reading, kanji, meaning)
    except (KeyError, IndexError, UnknownKana):
        return None


def load_pool(level: str = "jlpt-n5", max_pages: int = 10) -> list[dict]:
    """Fetch and cache a word pool, stopping early once pages come back empty."""
    for page in range(1, max_pages + 1):
        res = requests.get(
            API,
            params={"keyword": f"#{level}", "page": page},
            headers=HEADERS,
            timeout=5,
        )
        res.raise_for_status()
        data = res.json().get("data", [])
        if not data:
            break
        _pool.extend(q for e in data if (q := _to_question(e)) is not None)
        time.sleep(PAGE_DELAY)
    return _pool


def random_word() -> dict:
    """A random cached word. Raises IndexError if the pool is empty."""
    if not _pool:
        load_pool()
    return random.choice(_pool)
