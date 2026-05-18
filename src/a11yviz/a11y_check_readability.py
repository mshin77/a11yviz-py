"""Flesch-Kincaid grade and Flesch reading ease (WCAG 3.1.5)."""

import os
import re
from typing import Optional, Union

_vowel_group = re.compile(r"[aeiouy]+")
_word_re = re.compile(r"[A-Za-z']+")
_sent_re = re.compile(r"(?<=[.!?])\s+")
_fence_re = re.compile(r"```[\s\S]*?```")
_inline_re = re.compile(r"`[^`]*`")
_md_punct_re = re.compile(r"[#*_>~\[\]()]")


def a11y_check_readability(text: Union[str, os.PathLike]) -> dict:
    """Estimate reading level of prose

    Parameters
    ----------
    text
        Character vector, single string, or path to a .md, .qmd, .Rmd, or .txt file.

    Returns
    -------
        Data frame with one row and columns sentences, words, syllables, flesch_kincaid_grade, flesch_reading_ease.
    """
    text = _read_input(text)
    text = _strip_markdown(text)

    sentences = [s for s in _sent_re.split(text) if s.strip()]
    words = [w.lower() for w in _word_re.findall(text)]
    syllables = sum(_syllable_count(w) for w in words)

    n_sent, n_words = len(sentences), len(words)
    if n_sent == 0 or n_words == 0:
        return {"sentences": n_sent, "words": n_words, "syllables": syllables,
                "flesch_kincaid_grade": None, "flesch_reading_ease": None}

    asl = n_words / n_sent
    asw = syllables / n_words
    fk_grade = 0.39 * asl + 11.8 * asw - 15.59
    fk_ease  = 206.835 - 1.015 * asl - 84.6 * asw
    return {
        "sentences":            n_sent,
        "words":                n_words,
        "syllables":            syllables,
        "flesch_kincaid_grade": round(fk_grade, 2),
        "flesch_reading_ease":  round(fk_ease, 2),
    }


def _read_input(text) -> str:
    if isinstance(text, (str, os.PathLike)):
        path = os.fspath(text) if not isinstance(text, str) else text
        if path and os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                return fh.read()
    return str(text)


def _strip_markdown(text: str) -> str:
    text = _fence_re.sub(" ", text)
    text = _inline_re.sub(" ", text)
    return _md_punct_re.sub(" ", text)


def _syllable_count(word: str) -> int:
    if not word:
        return 0
    w = word.lower()
    if len(w) > 2 and w.endswith("e") and not w.endswith("le"):
        w = w[:-1]
    groups = _vowel_group.findall(w)
    return max(1, len(groups))
