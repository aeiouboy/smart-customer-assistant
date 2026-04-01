"""URL builder for Tops Online search integration."""

from urllib.parse import quote

from config import TOPS_SEARCH_BASE


def build_tops_search_url(keyword: str) -> str:
    """Encode Thai keyword and return Tops Online search URL."""
    if not keyword or not keyword.strip():
        return TOPS_SEARCH_BASE
    encoded = quote(keyword.strip(), safe="")
    return f"{TOPS_SEARCH_BASE}{encoded}"
