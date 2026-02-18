from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

TRACKING_QUERY_PREFIXES = ("utm_", "gclid", "fbclid")


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    filtered_query = [
        (k, v)
        for k, v in parse_qsl(parsed.query, keep_blank_values=True)
        if not any(k.startswith(prefix) for prefix in TRACKING_QUERY_PREFIXES)
    ]
    normalized = parsed._replace(fragment="", query=urlencode(sorted(filtered_query)))
    return urlunparse(normalized)


def same_origin(base_url: str, candidate_url: str) -> bool:
    return urlparse(base_url).netloc == urlparse(candidate_url).netloc


def is_denied_domain(candidate_url: str, denied_domains: list[str]) -> bool:
    host = urlparse(candidate_url).netloc.lower()
    return any(domain in host for domain in denied_domains)
