"""Configuration constants for Smart Customer Assistant."""

import os

from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model Configuration
MODEL_FAST = "google/gemini-2.5-flash"

# Tops Online Configuration
TOPS_SEARCH_BASE = "https://www.tops.co.th/th/search/"

# UI Colors
COLOR_SAFE = "#27AE60"
COLOR_WARN = "#E74C3C"
COLOR_TOPS_CTA = "#E31E24"

# Thresholds
CONFIDENCE_THRESHOLD = 0.6
