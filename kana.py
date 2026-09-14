"""Hiragana -> romaji conversion.

Grading a romaji answer is not a string comparison: most kana have more than
one accepted spelling (し = shi/si), so romanizations() returns the whole set
of valid answers and the caller checks membership.
"""
import itertools

SOKUON = "っ"


class UnknownKana(ValueError):
    """A character with no entry in ROMAJI."""


ROMAJI: dict[str, list[str]] = {
    "きゃ": ["kya"], "きゅ": ["kyu"], "きょ": ["kyo"],
    "しゃ": ["sha", "sya"], "しゅ": ["shu", "syu"], "しょ": ["sho", "syo"],
    "ちゃ": ["cha", "tya"], "ちゅ": ["chu", "tyu"], "ちょ": ["cho", "tyo"],
    "にゃ": ["nya"], "にゅ": ["nyu"], "にょ": ["nyo"],
    "ひゃ": ["hya"], "ひゅ": ["hyu"], "ひょ": ["hyo"],
    "みゃ": ["mya"], "みゅ": ["myu"], "みょ": ["myo"],
    "りゃ": ["rya"], "りゅ": ["ryu"], "りょ": ["ryo"],
    "ぎゃ": ["gya"], "ぎゅ": ["gyu"], "ぎょ": ["gyo"],
    "じゃ": ["ja", "jya", "zya"], "じゅ": ["ju", "jyu", "zyu"],
    "じょ": ["jo", "jyo", "zyo"],
    "ぢゃ": ["ja"], "ぢゅ": ["ju"], "ぢょ": ["jo"],
    "びゃ": ["bya"], "びゅ": ["byu"], "びょ": ["byo"],
    "ぴゃ": ["pya"], "ぴゅ": ["pyu"], "ぴょ": ["pyo"],

    "あ": ["a"], "い": ["i"], "う": ["u"], "え": ["e"], "お": ["o"],
    "か": ["ka"], "き": ["ki"], "く": ["ku"], "け": ["ke"], "こ": ["ko"],
    "さ": ["sa"], "し": ["shi", "si"], "す": ["su"], "せ": ["se"], "そ": ["so"],
    "た": ["ta"], "ち": ["chi", "ti"], "つ": ["tsu", "tu"], "て": ["te"], "と": ["to"],
    "な": ["na"], "に": ["ni"], "ぬ": ["nu"], "ね": ["ne"], "の": ["no"],
    "は": ["ha"], "ひ": ["hi"], "ふ": ["fu", "hu"], "へ": ["he"], "ほ": ["ho"],
    "ま": ["ma"], "み": ["mi"], "む": ["mu"], "め": ["me"], "も": ["mo"],
    "や": ["ya"], "ゆ": ["yu"], "よ": ["yo"],
    "ら": ["ra"], "り": ["ri"], "る": ["ru"], "れ": ["re"], "ろ": ["ro"],
    "わ": ["wa"], "を": ["wo", "o"], "ん": ["n"],

    "が": ["ga"], "ぎ": ["gi"], "ぐ": ["gu"], "げ": ["ge"], "ご": ["go"],
    "ざ": ["za"], "じ": ["ji", "zi"], "ず": ["zu"], "ぜ": ["ze"], "ぞ": ["zo"],
    "だ": ["da"], "ぢ": ["ji", "di"], "づ": ["zu", "du"], "で": ["de"], "ど": ["do"],
    "ば": ["ba"], "び": ["bi"], "ぶ": ["bu"], "べ": ["be"], "ぼ": ["bo"],
    "ぱ": ["pa"], "ぴ": ["pi"], "ぷ": ["pu"], "ぺ": ["pe"], "ぽ": ["po"],
}


def _geminate(romaji: str) -> list[str]:
    """Spellings of a syllable preceded by っ (the doubled consonant)."""
    if romaji.startswith("ch"):
        return ["t" + romaji, "c" + romaji]   # まっちゃ = matcha / maccha
    return [romaji[0] + romaji]


def _chunks(kana: str) -> list[tuple[str, bool]]:
    """Split kana into (syllable, preceded_by_sokuon) pairs."""
    out: list[tuple[str, bool]] = []
    i = 0
    while i < len(kana):
        geminate = kana[i] == SOKUON
        if geminate:
            i += 1
            if i >= len(kana):
                break
        if kana[i:i + 2] in ROMAJI:
            chunk = kana[i:i + 2]
        elif kana[i] in ROMAJI:
            chunk = kana[i]
        else:
            raise UnknownKana(kana[i])
        out.append((chunk, geminate))
        i += len(chunk)
    return out


def romanizations(kana: str) -> set[str]:
    """Every accepted romaji spelling of a hiragana string.

    Raises UnknownKana if the string contains anything unmappable.
    """
    chunks = _chunks(kana)
    parts: list[list[str]] = []
    for idx, (chunk, geminate) in enumerate(chunks):
        options = list(ROMAJI[chunk])
        if chunk == "ん" and idx + 1 < len(chunks):
            following = ROMAJI[chunks[idx + 1][0]][0]
            if following[0] in "bpm":
                options.append("m")
        if geminate:
            options = [spelling for o in options for spelling in _geminate(o)]
        parts.append(options)
    return {"".join(combo) for combo in itertools.product(*parts)}
