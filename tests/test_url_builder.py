"""Tests for url_builder.py — UNIT-URL-01 through UNIT-URL-04."""

import sys
import os
from urllib.parse import urlparse, unquote

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # ty: ignore[unresolved-import]
from url_builder import build_tops_search_url
from config import TOPS_SEARCH_BASE


class TestThaiKeywordEncoding:
    """UNIT-URL-01: Thai keyword is percent-encoded correctly."""

    def test_thai_milk_keyword_produces_url(self) -> None:
        """Thai 'นมสด' (fresh milk) is encoded and appended to the base URL."""
        result = build_tops_search_url("นมสด")
        assert result.startswith(TOPS_SEARCH_BASE)

    def test_thai_milk_keyword_is_percent_encoded(self) -> None:
        """Thai characters must be percent-encoded in the result URL."""
        result = build_tops_search_url("นมสด")
        # Decoded path should round-trip back to the original keyword
        suffix = result[len(TOPS_SEARCH_BASE):]
        assert unquote(suffix) == "นมสด"

    def test_thai_milk_keyword_no_raw_thai_in_url(self) -> None:
        """Raw Thai characters must not appear in the URL string."""
        result = build_tops_search_url("นมสด")
        assert "นมสด" not in result

    def test_thai_keyword_result_is_valid_url(self) -> None:
        """The returned string must be a parseable URL with scheme and netloc."""
        result = build_tops_search_url("นมสด")
        parsed = urlparse(result)
        assert parsed.scheme == "https"
        assert "tops.co.th" in parsed.netloc

    @pytest.mark.parametrize("keyword", [
        "นมสด",
        "ข้าวสาร",
        "ผลิตภัณฑ์นม",
        "กาแฟ",
        "น้ำมันพืช",
    ])
    def test_various_thai_keywords_are_encoded(self, keyword: str) -> None:
        """Parameterised: various Thai keywords should all produce encoded URLs."""
        result = build_tops_search_url(keyword)
        assert result.startswith(TOPS_SEARCH_BASE)
        suffix = result[len(TOPS_SEARCH_BASE):]
        assert unquote(suffix) == keyword.strip()


class TestSpecialCharactersEncoding:
    """UNIT-URL-02: Special characters are percent-encoded."""

    def test_ampersand_is_encoded(self) -> None:
        result = build_tops_search_url("salt & pepper")
        assert "&" not in result[len(TOPS_SEARCH_BASE):]

    def test_space_is_encoded(self) -> None:
        """Spaces must be encoded (not left as raw spaces or +)."""
        result = build_tops_search_url("fresh milk")
        suffix = result[len(TOPS_SEARCH_BASE):]
        assert " " not in suffix
        assert unquote(suffix) == "fresh milk"

    def test_hash_is_encoded(self) -> None:
        result = build_tops_search_url("item#1")
        suffix = result[len(TOPS_SEARCH_BASE):]
        assert "#" not in suffix

    def test_question_mark_is_encoded(self) -> None:
        result = build_tops_search_url("what?")
        suffix = result[len(TOPS_SEARCH_BASE):]
        assert "?" not in suffix

    def test_slash_is_encoded(self) -> None:
        result = build_tops_search_url("a/b")
        suffix = result[len(TOPS_SEARCH_BASE):]
        assert "/" not in suffix

    def test_mixed_thai_and_special_chars(self) -> None:
        """Thai text mixed with special chars should be fully encoded."""
        result = build_tops_search_url("นม & เนย")
        assert result.startswith(TOPS_SEARCH_BASE)
        suffix = result[len(TOPS_SEARCH_BASE):]
        assert unquote(suffix) == "นม & เนย"


class TestEmptyStringReturnsBaseUrl:
    """UNIT-URL-03: Empty string returns the base URL unchanged."""

    def test_empty_string_returns_base(self) -> None:
        result = build_tops_search_url("")
        assert result == TOPS_SEARCH_BASE

    def test_empty_string_no_trailing_junk(self) -> None:
        result = build_tops_search_url("")
        assert result == TOPS_SEARCH_BASE


class TestWhitespaceOnlyReturnsBaseUrl:
    """UNIT-URL-04: Whitespace-only strings return the base URL unchanged."""

    def test_single_space_returns_base(self) -> None:
        result = build_tops_search_url(" ")
        assert result == TOPS_SEARCH_BASE

    def test_multiple_spaces_returns_base(self) -> None:
        result = build_tops_search_url("   ")
        assert result == TOPS_SEARCH_BASE

    def test_tab_character_returns_base(self) -> None:
        result = build_tops_search_url("\t")
        assert result == TOPS_SEARCH_BASE

    def test_newline_character_returns_base(self) -> None:
        result = build_tops_search_url("\n")
        assert result == TOPS_SEARCH_BASE

    def test_mixed_whitespace_returns_base(self) -> None:
        result = build_tops_search_url("  \t  \n  ")
        assert result == TOPS_SEARCH_BASE

    def test_keyword_with_surrounding_whitespace_is_stripped(self) -> None:
        """Leading/trailing whitespace around a real keyword should be stripped."""
        result_padded = build_tops_search_url("  นมสด  ")
        result_clean = build_tops_search_url("นมสด")
        assert result_padded == result_clean
