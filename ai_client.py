"""AI client for product label analysis via OpenRouter/Gemini."""

import base64
import json

from openai import OpenAI  # ty: ignore[unresolved-import]

from config import MODEL_FAST, OPENROUTER_API_KEY, OPENROUTER_BASE_URL

SYSTEM_PROMPT = """You are a product label analysis expert. Analyze the product label image and return a JSON response with this EXACT structure:

{
  "product_info": {
    "brand_name": "brand name from label",
    "product_name": "product name from label",
    "clean_search_keyword": "concise Thai search keyword for online shopping"
  },
  "ingredients_analysis": {
    "additives_found": [
      {
        "name_th": "Thai name of additive",
        "purpose": "purpose in Thai (e.g., สารกันเสีย, สารแต่งสี, สารแต่งรส)",
        "risk_level": "Low or Medium or High"
      }
    ]
  },
  "health_dashboard": {
    "score": 75,
    "allergens_detected": ["list of allergens in Thai"],
    "verdict_th": "overall health verdict in Thai"
  },
  "metadata": {
    "ai_confidence_score": 0.85
  }
}

Rules:
- Decode ALL chemical names (E-numbers, MSG, preservatives) into plain Thai with their purpose
- Score health 0-100 based on nutritional value and additive safety
- Detect common allergens: gluten (กลูเตน), nuts (ถั่ว), dairy/milk (นม), shellfish (อาหารทะเล), soy (ถั่วเหลือง), eggs (ไข่)
- Set confidence score based on image clarity and readability
- Respond ONLY with valid JSON, no other text"""


def analyze_product_image(
    image_bytes: bytes, model: str = MODEL_FAST
) -> dict:
    """Send image to OpenRouter Gemini, return parsed JSON dict."""
    if not OPENROUTER_API_KEY:
        return {
            "error": True,
            "message": "OPENROUTER_API_KEY is not set. Please set the environment variable.",
        }

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
    )

    # Encode image as base64 data URL
    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{b64_image}"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this product label image and return the JSON analysis.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                },
            ],
            response_format={"type": "json_object"},
            max_tokens=2000,
        )

        content = response.choices[0].message.content
        if content is None:
            return {
                "error": True,
                "message": "AI returned an empty response. Please try again.",
            }
        result = json.loads(content)

        # Validate required keys
        required_keys = ["product_info", "ingredients_analysis", "health_dashboard", "metadata"]
        for key in required_keys:
            if key not in result:
                return {
                    "error": True,
                    "message": f"AI response missing required field: {key}",
                }

        return result

    except json.JSONDecodeError:
        return {
            "error": True,
            "message": "AI returned invalid JSON. Please try again with a clearer image.",
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"API error: {e!s}",
        }
