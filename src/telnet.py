from scrambler import scramble_emails
from collections import defaultdict
from dig import get_mx_servers
from telnetlib import Telnet
from itertools import cycle
from os.path import exists
from sys import argv

# smtp normal port. TODO: think of a fallback port scan in case of failure
SMTP_PORT = 25

ENTER = b"\r\n"


def telnet_connect(host: str, email: str) -> [str]:
    print(f"\nStarting Telnet <{host}>...")
    # start a Telnet instance. (TODO: watch out for timeouts)
    # if connection refused, try disconnecting from your VPN

    with Telnet(host, SMTP_PORT) as tn:
        tn.write(b"EHLO mail.gmail.com" + ENTER)
        tn.write(b"MAIL FROM: <example@gmail.com>" + ENTER)
        print(f"Connected to {host}")

        check_str = f"RCPT TO: <{email}>"
        print(f"Checking email: {check_str}")
        tn.write(check_str.encode() + ENTER)

        tn.write(b"QUIT" + ENTER)
        output = tn.read_all()
        print(f"Disconnecting from <{host}>")
        return output.decode('utf8').lower().splitlines()


def get_response_by_code(telnet_response_lines: [str]) -> bool:
    response_by_code = defaultdict(list)
    for line in telnet_response_lines:
        code, *rest = line.split(" ")
        response_by_code[code].append(' '.join(rest))
    return response_by_code


hosts_by_domain = defaultdict(list)


def verify_email(email: str) -> dict:
    _, domain = email.split("@")

    if domain not in hosts_by_domain:
        hosts_by_domain[domain] = cycle(get_mx_servers(domain))
    hosts = hosts_by_domain.get(domain)
    host = next(hosts)

    response_telnet_by_lines = telnet_connect(host, email)
    response_by_code = get_response_by_code(response_telnet_by_lines)
    is_valid = sum("ok" in res for res in response_by_code["250"]) == 2
    return {"email": email, "is_valid": is_valid, "error": None}


def verify_emails(emails: [str]) -> dict:
    return list(map(verify_email, emails))


def main(domain):
    # sample emails or scrambler
    # TODO: build list from text file or get the option to scrape page + linkedin + google...
    usernames_path = "./usernames.txt"
    if exists(usernames_path):
        with open(usernames_path, "r") as file:
            usernames = file.read().splitlines()
        if not usernames:
            print("Usernames file empty.")
            return
    else:
        usernames = ["support"]

    # scramble domain with potential usernames
    emails = scramble_emails(domain, usernames)
    verifications = verify_emails(emails)
    print(verifications)

    print("\n--- Results:")
    for email in verifications.keys():
        is_valid = verifications[email].get('is_valid')
        print("{}VALID: {}".format("" if is_valid else "NOT ", email))


def check_domain(domain: str) -> str or error:
    pass


if __name__ == "__main__":
    # get through user input
    # if len(argv) < 2:
    #     domain = input("Input a domain: ")
    # else:
    #     domain = argv[1]
    # main(domain)

    result = verify_email("victor.momparler@ovoenergy.com")
    print(result)
