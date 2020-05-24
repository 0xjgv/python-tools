from datetime import datetime, timedelta
from json import dumps, loads
from typing import Callable
from itertools import cycle
from random import randint
from os.path import exists
from smtplib import SMTP
from re import search


EMAIL_VERIFICATIONS = "./cache/verifications.ldjson"
REQUEST_TIMEOUT_SMTP = 25
EMAILS_LIST = "emails.csv"
DATE_FORMAT = "%Y-%m-%d"


# Caching mechanism
# def verify_email_middleware(fn):
#     now = datetime.now().strftime(DATE_FORMAT)
#     emails = {}
#     if exists(EMAIL_VERIFICATIONS):
#         with open(EMAIL_VERIFICATIONS, 'r') as file:
#             for line in file.readlines():
#                 line_json = loads(line)
#                 emails[line_json.get("email")] = line_json

#     def wrapper(email):
#         if email not in emails:
#             result = {**fn(email), 'date': now}
#             try:
#                 with open(EMAIL_VERIFICATIONS, 'a') as file:
#                     file.write(dumps(result) + "\n")
#             except Exception as exc:
#                 print(exc)
#             return result
#         return emails.get(email)

#     return wrapper


def smtp_email_check(mx: str, username: str, domain: str) -> (int, bytes):
    email = f"{username}@{domain}"
    proxy_address = ("", 9150)
    try:
        with SMTP(
            mx, timeout=REQUEST_TIMEOUT_SMTP, source_address=proxy_address
        ) as smtp:
            smtp.ehlo(f"mail.{domain}")
            smtp.docmd(f"mail from: <{email}>")
            return smtp.docmd(f"rcpt to: <{email}>")
    except Exception as exc:
        print(exc)
        return 502, str(exc).encode()


hosts_by_domain = {}


MAX_RETRIES = 10
# Caching mechanism
# @verify_email_middleware
def verify_email(email: str, get_mx_servers: Callable) -> dict:
    if not "@" in email:
        return {"email": email, "error": "Not an email."}
    username, domain = email.split("@")

    if domain not in hosts_by_domain:
        hosts_by_domain[domain] = cycle(get_mx_servers(domain))

    hosts = hosts_by_domain.get(domain)
    for i, host in enumerate(hosts):
        code, msg = smtp_email_check(host, username, domain)
        is_valid = code == 250
        error = msg.decode() if not is_valid else None
        if error and "48" in error:
            if i > MAX_RETRIES:
                break
            continue
        return {"email": email, "is_valid": is_valid, "error": error, "host": host}

    return {"email": email, "error": f"Host not found for {domain} domain."}


if __name__ == "__main__":
    from dig import get_mx_servers

    res = verify_email("example@gmail.com", get_mx_servers)
    print(res)
