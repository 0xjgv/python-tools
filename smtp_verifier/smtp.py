from time import sleep
from typing import Callable, Tuple
from itertools import cycle
from smtplib import SMTP


EMAIL_VERIFICATIONS = "./cache/verifications.ldjson"
REQUEST_TIMEOUT_SMTP = 25
EMAILS_LIST = "emails.csv"
DATE_FORMAT = "%Y-%m-%d"


def smtp_email_check(mx: str, username: str, domain: str) -> Tuple[int, bytes]:
    email = f"{username}@{domain}"
    proxy_address = ("", 9150)
    try:
        with SMTP(mx, timeout=REQUEST_TIMEOUT_SMTP, source_address=proxy_address) as smtp:
            smtp.ehlo(f"mail.{domain}")
            smtp.docmd(f"mail from: <{email}>")
            return smtp.docmd(f"rcpt to: <{email}>")
    except Exception as exc:
        return 502, str(exc).encode()


hosts_by_domain = {}


MAX_RETRIES = 10


def verify_email(email: str, get_mx_servers: Callable) -> dict:
    if "@" not in email:
        return {"email": email, "error": "Not an email."}
    username, domain = email.split("@")

    if domain not in hosts_by_domain:
        hosts_by_domain[domain] = cycle(get_mx_servers(domain))

    for i, host in enumerate(hosts_by_domain.get(domain, [])):
        code, msg = smtp_email_check(host, username, domain)
        is_valid = code == 250
        error = msg.decode() if not is_valid else None
        if error and "48" in error:
            sleep(1)
            if i > MAX_RETRIES:
                break
            continue
        return {"email": email, "is_valid": is_valid, "error": error, "host": host}

    return {"email": email, "error": f"Host not found for {domain} domain."}


def verify_domain_most_common(domain: str, get_mx_servers: Callable) -> dict:
    if mx_servers := get_mx_servers(domain):
        hosts_by_domain[domain] = cycle(mx_servers)
    else:
        return {"domain": domain, "error": f"MX servers not found for {domain} domain."}

    usernames = []
    with open("./smtp_verifier/common_email_usernames.txt", "r") as file:
        for username in map(str.strip, file.readlines()):
            usernames.append(username)
            if username[-1] not in "aeiou":
                # Pluralized
                usernames.append(f"{username}s")

    results = {}
    for username in usernames:
        results[username] = verify_email(f"{username}@{domain}", get_mx_servers)
    return results


if __name__ == "__main__":
    from dig import get_mx_servers

    res = verify_domain_most_common("revolut.ar", get_mx_servers)
    for k, v in res.items():
        print(k, v)
