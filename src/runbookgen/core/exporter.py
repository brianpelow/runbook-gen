"""Runbook export to Markdown and Confluence."""

from __future__ import annotations

import os
from pathlib import Path


def export_to_markdown(content: str, output_path: Path) -> Path:
    """Write runbook content to a Markdown file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)
    return output_path


def export_to_confluence(content: str, title: str, space_key: str = "ENG") -> bool:
    """Export runbook to Confluence via REST API."""
    base_url = os.environ.get("CONFLUENCE_URL", "")
    token = os.environ.get("CONFLUENCE_TOKEN", "")

    if not base_url or not token:
        return False

    try:
        import httpx
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": _markdown_to_confluence(content),
                    "representation": "storage",
                }
            },
        }
        response = httpx.post(
            f"{base_url}/rest/api/content",
            json=payload,
            headers=headers,
            timeout=30,
        )
        return response.status_code in (200, 201)
    except Exception:
        return False


def _markdown_to_confluence(markdown: str) -> str:
    """Basic markdown to Confluence storage format conversion."""
    content = markdown
    import re
    content = re.sub(r"^# (.+)$", r"<h1>\1</h1>", content, flags=re.MULTILINE)
    content = re.sub(r"^## (.+)$", r"<h2>\1</h2>", content, flags=re.MULTILINE)
    content = re.sub(r"^### (.+)$", r"<h3>\1</h3>", content, flags=re.MULTILINE)
    content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", content)
    content = re.sub(r"```[\w]*\n(.*?)```", r"<code>\1</code>", content, flags=re.DOTALL)
    return content