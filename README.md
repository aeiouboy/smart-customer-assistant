# Smart Customer Assistant

An AI-powered product label analyzer built with Streamlit and OpenRouter. Upload or photograph a product label and instantly receive a health score, allergen alerts, additive breakdowns, and a direct link to buy the product on Tops Online.

## Features

- Camera capture or image upload (JPG, PNG, WebP)
- AI-powered label analysis via Google Gemini (through OpenRouter)
- Health score from 0–100 based on nutritional value and additive safety
- Allergen detection: gluten, nuts, dairy, shellfish, soy, eggs
- Decoded additive list with risk levels (Low / Medium / High)
- AI confidence score with a visual progress bar
- One-click shopping link to Tops Online for the identified product

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- An [OpenRouter](https://openrouter.ai/) API key with access to Gemini models

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Set the API key

Either export the variable in your shell:

```bash
export OPENROUTER_API_KEY=sk-or-v1-xxxx
```

Or create a `.env` file in the `smart-assistant/` directory:

```
OPENROUTER_API_KEY=sk-or-v1-xxxx
```

### 3. Run the application

```bash
uv run streamlit run app.py
```

The app opens in your browser at `http://localhost:8501` by default.

## Usage

1. Click **ถ่ายรูปฉลากสินค้า** to use your webcam, or **อัปโหลดรูปภาพ** to upload a file.
2. Press the **วิเคราะห์สินค้า** button.
3. Review the health dashboard: product info, health score, allergens, and additive table.
4. Click the **สั่งซื้อที่ Tops Online** button to open the product search on Tops Online.

## Architecture

The application is composed of four modules:

| Module | Responsibility |
|---|---|
| `app.py` | Streamlit UI orchestrator; manages session state and renders the dashboard |
| `ai_client.py` | OpenRouter/Gemini integration; encodes images, calls the API, parses JSON |
| `url_builder.py` | Encodes Thai keywords into Tops Online search URLs |
| `config.py` | Centralizes constants: API key, model name, color codes, thresholds |

### Data flow

```
User uploads image
    → app.py reads image bytes
    → ai_client.py encodes to base64 and calls OpenRouter API
    → Gemini returns structured JSON
    → app.py renders health dashboard
    → url_builder.py builds Tops Online search URL
    → User clicks CTA link to Tops Online
```

## Project Structure

```
smart-assistant/
├── app.py           # Streamlit application entry point
├── ai_client.py     # OpenRouter / Gemini API client
├── url_builder.py   # Tops Online URL encoder
├── config.py        # Configuration constants and environment variables
├── pyproject.toml   # Project metadata and dependencies
└── tests/           # Automated test suite
```

## Running Tests

```bash
uv run pytest tests/
```

## Further Reading

- [Environment Setup](../docs/env-setup.md)
- [Architecture](../docs/architecture.md)
- [Troubleshooting](../docs/troubleshooting.md)
