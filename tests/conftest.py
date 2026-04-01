"""Shared fixtures for Smart Customer Assistant tests."""

import pytest  # ty: ignore[unresolved-import]


@pytest.fixture
def sample_image_bytes() -> bytes:
    """Return minimal valid JPEG bytes for testing."""
    # A minimal 1x1 JPEG
    return bytes([
        0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01,
        0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
        0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09,
        0x09, 0x08, 0x0A, 0x0C, 0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
        0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D, 0x1A, 0x1C, 0x1C, 0x20,
        0x24, 0x2E, 0x27, 0x20, 0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29,
        0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27, 0x39, 0x3D, 0x38, 0x32,
        0x3C, 0x2E, 0x33, 0x34, 0x32, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01,
        0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x1F, 0x00, 0x00,
        0x01, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
        0x09, 0x0A, 0x0B, 0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01, 0x00, 0x00, 0x3F,
        0x00, 0xFB, 0xFF, 0xD9,
    ])


@pytest.fixture
def valid_api_response() -> dict:
    """Return a valid API response structure matching the expected schema."""
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
                },
                {
                    "name_th": "แคลเซียม",
                    "purpose": "สารเสริมแร่ธาตุ",
                    "risk_level": "Low",
                },
            ]
        },
        "health_dashboard": {
            "score": 85,
            "allergens_detected": ["นม"],
            "verdict_th": "ผลิตภัณฑ์นี้มีคุณภาพดี เหมาะสำหรับการบริโภค",
        },
        "metadata": {
            "ai_confidence_score": 0.92,
        },
    }


@pytest.fixture
def error_api_response() -> dict:
    """Return a typical error response dict."""
    return {
        "error": True,
        "message": "API error: something went wrong",
    }


@pytest.fixture
def valid_api_response_low_score() -> dict:
    """Return a valid API response with a low health score."""
    return {
        "product_info": {
            "brand_name": "TestBrand",
            "product_name": "ขนมขบเคี้ยว",
            "clean_search_keyword": "ขนมขบเคี้ยว TestBrand",
        },
        "ingredients_analysis": {
            "additives_found": [
                {
                    "name_th": "ผงชูรส (MSG)",
                    "purpose": "สารแต่งรส",
                    "risk_level": "High",
                },
                {
                    "name_th": "สีสังเคราะห์ E102",
                    "purpose": "สารแต่งสี",
                    "risk_level": "Medium",
                },
            ]
        },
        "health_dashboard": {
            "score": 30,
            "allergens_detected": ["กลูเตน", "ถั่วเหลือง"],
            "verdict_th": "ผลิตภัณฑ์นี้มีสารปรุงแต่งสูง ควรบริโภคในปริมาณน้อย",
        },
        "metadata": {
            "ai_confidence_score": 0.78,
        },
    }
