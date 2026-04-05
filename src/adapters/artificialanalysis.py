"""Adapter for artificialanalysis.ai leaderboard.

FETCH: Retrieves raw HTML from the source URL.
PARSE: Extracts embedded JSON from Next.js RSC payload and converts to model dicts.

SCHEMA_VERSION 1:
  - Next.js React Server Components use encoded push calls: self.__next_f.push([1, "18:..."])
  - The data is stored in Script 54 (>50k chars), starting with {"models":[{...model...},...]}
  - All source-specific fields go into `extras` dict.
"""

import logging
import re
import json

import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

SCHEMA_VERSION = 1


def fetch(url: str) -> str:
    """Fetch raw HTML from URL. Raises on HTTP errors."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def parse(html: str, schema_ver: int = SCHEMA_VERSION) -> list[dict]:
    """Parse artificialanalysis.ai HTML into list of model dicts.

    The page is Next.js with React Server Components. Model data is embedded in a
    large <script> tag as a self.__next_f.push([1, "18:..."]) call where the
    second argument is a JSON string containing {"models":[{...},...]}.

    Returns list of dicts:
      [{model_name: str, org: str, score: float, ...}, ...]
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = []

    # Find the large script with model data (>50k chars)
    scripts = soup.find_all("script")
    big_script = None
    for script in scripts:
        content = script.string or ""
        if len(content) > 50000 and "models" in content:
            big_script = content
            break

    if not big_script:
        log.warning("No model data script found in artificialanalysis.ai response")
        return rows

    # The script content is an encoded string inside: self.__next_f.push([1, "18:..."])
    # Find the index where {"models": appears in the decoded string
    # The escaped form is \"models\":[
    models_escaped = '\\"models":['
    idx = big_script.find(models_escaped)
    if idx < 0:
        log.warning("Could not find models array in script")
        return rows

    # Extract the JSON from the escaped string
    # The array is at the end of the string: after \"models\":[  ...  }]
    # We need to find where the array ends by bracket matching
    array_start = idx + len(models_escaped)
    # Find the next object start {
    chunk = big_script[array_start:]
    # Find the closing ] for the models array - it ends with ...}]}}
    # Actually the pattern ends with: ...}]} and then ]
    # Let's extract a reasonable chunk and parse

    # From the debug output: The pattern ends with ...]}]\n
    # So we find the double closing }}
    end_idx = chunk.find('}]')
    if end_idx < 0:
        log.warning("Could not find end of models array")
        return rows

    # Extract and assemble the JSON array
    json_str = '[' + chunk[:end_idx + 1]

    # Unescape the string: \q becomes " etc.
    # The HTML contains \\"  which should be "
    json_str_unescaped = json_str.replace('\\"', '"')

    try:
        models = json.loads(json_str_unescaped)
    except json.JSONDecodeError as e:
        log.warning(f"Failed to parse models JSON: {e}")
        log.info(f"JSON string (first 300): {json_str_unescaped[:300]}")
        return rows

    log.info(f"Parsed {len(models)} models from artificialanalysis.ai")

    for model in models:
        creator = model.get("creator", {})
        row = {
            "model_name": model.get("name", ""),
            "extras": {
                "slug": model.get("slug", ""),
                "org": creator.get("name", ""),
                "org_color": creator.get("color", ""),
                "deprecated": model.get("deprecated", False),
                "is_reasoning": model.get("isReasoning", False),
            },
            "schema_version": schema_ver,
        }

        # Additional top-level fields from model object
        for field in ("shortName", "url"):
            if field in model:
                row["extras"][field] = model[field]

        rows.append(row)

    return rows
