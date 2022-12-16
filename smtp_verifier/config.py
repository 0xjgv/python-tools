from pathlib import Path
from datetime import datetime


CACHE_PATH = Path(Path.home(), ".cache/smtp_verifier")
if not CACHE_PATH.exists():
    CACHE_PATH.mkdir(exist_ok=True)

LOG_ENTRY_PATH = Path(CACHE_PATH, "verifications.log")

MX_DOMAINS_PATH = Path(CACHE_PATH, "mx_by_domain.json")

REQUEST_TIMEOUT_SMTP = 25
EMAILS_LIST = "emails.csv"
DATE_FORMAT = "%Y-%m-%d"


def log_entry(fn):
    LOG_ENTRY_PATH.touch(exist_ok=True)

    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        with LOG_ENTRY_PATH.open(mode="a") as log:
            timestamp = datetime.now().isoformat()
            info = ", ".join([f"{k}={v}" for k, v in result.items()])
            log.writelines([f"[{timestamp}] {info}", "\n"])
        return result

    return wrapper
