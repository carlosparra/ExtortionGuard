from app.schemas.urlcheck import URLCheckOut
from app.core.config import settings
import requests


SUSPICIOUS_HOSTS = ("bit.ly", "tinyurl.com", "t.co", "wa.me", "linktr.ee")


WEBRISK_ENDPOINT = (
"https://webrisk.googleapis.com/v1/uris:search?threatTypes=SOCIAL_ENGINEERING,MALWARE,UNWANTED_SOFTWARE&uri={url}&key={key}"
)


def check_url(url: str) -> URLCheckOut:
    u = url.lower()
    if any(h in u for h in SUSPICIOUS_HOSTS):
        return URLCheckOut(unsafe=True, reason="shortener/suspicious host (heuristic)")
    return URLCheckOut(unsafe=False)




def check_url_v2(url: str) -> URLCheckOut:
    if settings.SAFE_BROWSING_KEY:
        try:
            r = requests.get(WEBRISK_ENDPOINT.format(url=url, key=settings.SAFE_BROWSING_KEY), timeout=5)
            r.raise_for_status()
            data = r.json()
            if data.get("threat"):
                t = ",".join(data["threat"].get("threatTypes", ["risk"]))
                return URLCheckOut(unsafe=True, reason=t or "webrisk")
        except Exception:
            pass
    return check_url(url)