"""Tests for config.py constants — UNIT-CFG-01, UNIT-CFG-02."""

import sys
import os

# Ensure the smart-assistant package root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


class TestConfigDefaults:
    """UNIT-CFG-01: Default config values are correct."""

    def test_openrouter_base_url(self) -> None:
        assert config.OPENROUTER_BASE_URL == "https://openrouter.ai/api/v1"

    def test_model_fast_value(self) -> None:
        assert config.MODEL_FAST == "google/gemini-flash-1.5"

    def test_color_safe_hex(self) -> None:
        assert config.COLOR_SAFE == "#27AE60"

    def test_color_warn_hex(self) -> None:
        assert config.COLOR_WARN == "#E74C3C"

    def test_color_tops_cta_hex(self) -> None:
        assert config.COLOR_TOPS_CTA == "#E31E24"

    def test_confidence_threshold_is_float(self) -> None:
        assert isinstance(config.CONFIDENCE_THRESHOLD, float)

    def test_confidence_threshold_value(self) -> None:
        assert config.CONFIDENCE_THRESHOLD == 0.6

    def test_openrouter_api_key_is_string(self) -> None:
        # Key may be empty string when env var not set; must be a string
        assert isinstance(config.OPENROUTER_API_KEY, str)


class TestTopsSearchBaseUrl:
    """UNIT-CFG-02: TOPS_SEARCH_BASE URL format is correct."""

    def test_tops_search_base_starts_with_https(self) -> None:
        assert config.TOPS_SEARCH_BASE.startswith("https://")

    def test_tops_search_base_points_to_tops(self) -> None:
        assert "tops.co.th" in config.TOPS_SEARCH_BASE

    def test_tops_search_base_ends_with_slash(self) -> None:
        # Must end with slash so encoded keyword appends cleanly
        assert config.TOPS_SEARCH_BASE.endswith("/")

    def test_tops_search_base_exact_value(self) -> None:
        assert config.TOPS_SEARCH_BASE == "https://www.tops.co.th/th/search/"
