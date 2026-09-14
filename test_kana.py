import pytest  

from kana import UnknownKana, romanizations


def test_plain_word() -> None:
    assert romanizations("にほん") == {"nihon"}


def test_alternate_spellings() -> None:
    assert romanizations("すし") == {"sushi", "susi"}


def test_digraph_is_one_syllable() -> None:
    assert "kaisha" in romanizations("かいしゃ")
    assert "kaisya" in romanizations("かいしゃ")
    assert "kaishiya" not in romanizations("かいしゃ")


def test_sokuon_doubles_next_consonant() -> None:
    assert romanizations("けっこん") == {"kekkon"}
    assert romanizations("きって") == {"kitte"}


def test_sokuon_before_ch() -> None:
    assert romanizations("まっちゃ") == {"matcha", "maccha", "mattya"}


def test_trailing_sokuon_is_dropped() -> None:
    assert romanizations("あっ") == {"a"}


def test_n_before_labial_may_be_m() -> None:
    spellings = romanizations("しんぶん")
    assert "shinbun" in spellings
    assert "shimbun" in spellings


def test_n_elsewhere_is_only_n()  -> None:
    assert romanizations("にほん") == {"nihon"}


def test_long_vowel_is_literal() -> None:
    assert romanizations("とうきょう") == {"toukyou"}


def test_unmapped_character_raises() -> None:
    with pytest.raises(UnknownKana):
        romanizations("カタカナ")
