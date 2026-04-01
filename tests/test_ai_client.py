"""Tests for ai_client.py — UNIT-AI-01 through UNIT-AI-08."""

import sys
import os
import json
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # ty: ignore[unresolved-import]


# ---------------------------------------------------------------------------
# Helpers to build mock OpenAI response objects
# ---------------------------------------------------------------------------

def _make_mock_response(content: str | None) -> MagicMock:
    """Build a minimal mock that mirrors openai.ChatCompletion response shape."""
    mock_message = MagicMock()
    mock_message.content = content

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    return mock_response


def _make_valid_payload() -> dict:
    return {
        "product_info": {
            "brand_name": "Meiji",
            "product_name": "นมสด UHT",
            "clean_search_keyword": "นมสด Meiji UHT",
        },
        "ingredients_analysis": {
            "additives_found": [
                {
                    "name_th": "วิตามิน D",
                    "purpose": "สารเสริมวิตามิน",
                    "risk_level": "Low",
                }
            ]
        },
        "health_dashboard": {
            "score": 85,
            "allergens_detected": ["นม"],
            "verdict_th": "ผลิตภัณฑ์นี้มีคุณภาพดี",
        },
        "metadata": {
            "ai_confidence_score": 0.92,
        },
    }


# ---------------------------------------------------------------------------
# UNIT-AI-01: Valid JSON response is parsed correctly
# ---------------------------------------------------------------------------

class TestValidJsonResponseParsed:
    """UNIT-AI-01: Valid JSON response is parsed into a dict without error."""

    def test_returns_dict(self, sample_image_bytes: bytes) -> None:
        payload = _make_valid_payload()
        mock_resp = _make_mock_response(json.dumps(payload))

        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert isinstance(result, dict)
        assert "error" not in result

    def test_product_info_key_present(self, sample_image_bytes: bytes) -> None:
        payload = _make_valid_payload()
        mock_resp = _make_mock_response(json.dumps(payload))

        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
             patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert "product_info" in result

    def test_brand_name_parsed(self, sample_image_bytes: bytes) -> None:
        payload = _make_valid_payload()
        mock_resp = _make_mock_response(json.dumps(payload))

        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
             patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result["product_info"]["brand_name"] == "Meiji"


# ---------------------------------------------------------------------------
# UNIT-AI-02: All required keys are present in a valid response
# ---------------------------------------------------------------------------

class TestRequiredKeysPresent:
    """UNIT-AI-02: Valid response contains all four required top-level keys."""

    @pytest.mark.parametrize("key", [
        "product_info",
        "ingredients_analysis",
        "health_dashboard",
        "metadata",
    ])
    def test_required_key_present(self, key: str, sample_image_bytes: bytes) -> None:
        payload = _make_valid_payload()
        mock_resp = _make_mock_response(json.dumps(payload))

        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
             patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert key in result


# ---------------------------------------------------------------------------
# UNIT-AI-03: Score range 0-100 is valid
# ---------------------------------------------------------------------------

class TestScoreRange:
    """UNIT-AI-03: Health score value from response is within 0-100."""

    @pytest.mark.parametrize("score", [0, 1, 50, 75, 99, 100])
    def test_score_within_valid_range(self, score: int, sample_image_bytes: bytes) -> None:
        payload = _make_valid_payload()
        payload["health_dashboard"]["score"] = score
        mock_resp = _make_mock_response(json.dumps(payload))

        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
             patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert 0 <= result["health_dashboard"]["score"] <= 100


# ---------------------------------------------------------------------------
# UNIT-AI-04: Additives list is parsed
# ---------------------------------------------------------------------------

class TestAdditivesListParsed:
    """UNIT-AI-04: Additives list in ingredients_analysis is parsed as a list."""

    def test_additives_found_is_list(self, sample_image_bytes: bytes) -> None:
        payload = _make_valid_payload()
        mock_resp = _make_mock_response(json.dumps(payload))

        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
             patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert isinstance(result["ingredients_analysis"]["additives_found"], list)

    def test_additive_has_expected_keys(self, sample_image_bytes: bytes) -> None:
        payload = _make_valid_payload()
        mock_resp = _make_mock_response(json.dumps(payload))

        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
             patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        first_additive = result["ingredients_analysis"]["additives_found"][0]
        assert "name_th" in first_additive
        assert "purpose" in first_additive
        assert "risk_level" in first_additive

    def test_empty_additives_list_is_valid(self, sample_image_bytes: bytes) -> None:
        payload = _make_valid_payload()
        payload["ingredients_analysis"]["additives_found"] = []
        mock_resp = _make_mock_response(json.dumps(payload))

        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
             patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result["ingredients_analysis"]["additives_found"] == []


# ---------------------------------------------------------------------------
# UNIT-AI-05: Missing API key returns error dict
# ---------------------------------------------------------------------------

class TestMissingApiKey:
    """UNIT-AI-05: When OPENROUTER_API_KEY is empty, function returns error dict."""

    def test_returns_error_true(self, sample_image_bytes: bytes) -> None:
        with patch("ai_client.OPENROUTER_API_KEY", ""):
            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result.get("error") is True

    def test_error_message_mentions_api_key(self, sample_image_bytes: bytes) -> None:
        with patch("ai_client.OPENROUTER_API_KEY", ""):
            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert "OPENROUTER_API_KEY" in result.get("message", "")

    def test_no_network_call_when_key_missing(self, sample_image_bytes: bytes) -> None:
        with patch("ai_client.OPENROUTER_API_KEY", ""), \
             patch("ai_client.OpenAI") as mock_openai_cls:
            import ai_client
            ai_client.analyze_product_image(sample_image_bytes)
            mock_openai_cls.assert_not_called()


# ---------------------------------------------------------------------------
# UNIT-AI-06: API exception returns error dict
# ---------------------------------------------------------------------------

class TestApiExceptionReturnsError:
    """UNIT-AI-06: When the OpenAI client raises an exception, an error dict is returned."""

    def test_returns_error_true_on_exception(self, sample_image_bytes: bytes) -> None:
        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.side_effect = Exception("Connection refused")
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result.get("error") is True

    def test_error_message_contains_exception_text(self, sample_image_bytes: bytes) -> None:
        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.side_effect = Exception("Connection refused")
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert "Connection refused" in result.get("message", "")

    def test_timeout_exception_returns_error(self, sample_image_bytes: bytes) -> None:
        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.side_effect = TimeoutError("Request timed out")
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result.get("error") is True


# ---------------------------------------------------------------------------
# UNIT-AI-07: Invalid JSON response returns error dict
# ---------------------------------------------------------------------------

class TestInvalidJsonReturnsError:
    """UNIT-AI-07: When AI returns non-JSON content, an error dict is returned."""

    def test_plain_text_response_returns_error(self, sample_image_bytes: bytes) -> None:
        mock_resp = _make_mock_response("Sorry, I cannot analyze this image.")

        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result.get("error") is True

    def test_truncated_json_returns_error(self, sample_image_bytes: bytes) -> None:
        mock_resp = _make_mock_response('{"product_info": {"brand_name":')

        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result.get("error") is True

    def test_invalid_json_message_is_helpful(self, sample_image_bytes: bytes) -> None:
        mock_resp = _make_mock_response("not json at all")

        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        # Message should not be empty
        assert result.get("message", "") != ""

    def test_missing_required_key_returns_error(self, sample_image_bytes: bytes) -> None:
        """JSON is valid but missing a required top-level key."""
        incomplete = {
            "product_info": {"brand_name": "Test"},
            "ingredients_analysis": {"additives_found": []},
            # Missing health_dashboard and metadata
        }
        mock_resp = _make_mock_response(json.dumps(incomplete))

        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result.get("error") is True


# ---------------------------------------------------------------------------
# UNIT-AI-08: Null content response returns error dict
# ---------------------------------------------------------------------------

class TestNullContentReturnsError:
    """UNIT-AI-08: When AI response content is None, an error dict is returned."""

    def test_none_content_returns_error(self, sample_image_bytes: bytes) -> None:
        mock_resp = _make_mock_response(None)

        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result.get("error") is True

    def test_none_content_error_message_not_empty(self, sample_image_bytes: bytes) -> None:
        mock_resp = _make_mock_response(None)

        with patch("ai_client.OpenAI") as mock_openai_cls, \
             patch("ai_client.OPENROUTER_API_KEY", "test-key"):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_resp
            mock_openai_cls.return_value = mock_client

            import ai_client
            result = ai_client.analyze_product_image(sample_image_bytes)

        assert result.get("message", "") != ""
