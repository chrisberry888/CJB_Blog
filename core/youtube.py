import re
from urllib.parse import parse_qs, urlparse

YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def _clean_candidate(value):
    candidate = (value or "").strip().split("?")[0].split("&")[0].strip("/")
    if YOUTUBE_ID_RE.match(candidate):
        return candidate
    return ""


def extract_youtube_video_id(url):
    """Extract a video id from common YouTube URL forms, or return an empty string."""
    raw_value = (url or "").strip()
    if not raw_value:
        return ""

    direct_id = _clean_candidate(raw_value)
    if direct_id:
        return direct_id

    parsed = urlparse(raw_value)
    host = parsed.netloc.lower().replace("www.", "")
    path_parts = [part for part in parsed.path.split("/") if part]

    if host == "youtu.be" and path_parts:
        return _clean_candidate(path_parts[0])

    if host.endswith("youtube.com"):
        if parsed.path == "/watch":
            query_id = parse_qs(parsed.query).get("v", [""])[0]
            return _clean_candidate(query_id)

        if path_parts and path_parts[0] in {"embed", "shorts", "live"} and len(path_parts) > 1:
            return _clean_candidate(path_parts[1])

    return ""

