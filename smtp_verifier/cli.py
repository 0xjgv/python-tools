from argparse import ArgumentParser, Namespace
from smtp_verifier.dig import get_mx_servers
from smtp_verifier.smtp import verify_email
from typing import List
import sys


def parse_options(args: List[str]) -> Namespace:
    parser = ArgumentParser(description="SMTP tool to verify emails")
    subparser = parser.add_subparsers(help="commands", dest="command", required=True)

    verify_parser = subparser.add_parser("verify", help="Verify an email (not always possible)")
    verify_parser.add_argument("email", type=str, help="Email to check", nargs="+")

    mx_parser = subparser.add_parser("mx", help="Get MX records for a domain or email")
    mx_parser.add_argument("domain", metavar="domain|email", type=str, nargs="+")

    return parser.parse_args(args)


def run(args: Namespace) -> None:
    if args.command == "verify":
        mxs = {}
        for email in args.email:
            print("Verifying:", email)
            verification = verify_email(email, get_mx_servers)
            print("Verification:", verification)
    elif args.command == "mx":
        for d in args.domain:
            domain = d
            if "@" in domain:
                _, domain = domain.split("@")
            elif "." not in domain:
                raise ValueError("A valid domain|email is required.")
            mxs = get_mx_servers(domain)
            print(f"MX hosts for {d}:", ", ".join(mxs))


def main():
    if sys.stdin.isatty():
        run(parse_options(sys.argv[1:]))
    else:
        lines = list(map(str.strip, sys.stdin))
        run(parse_options(sys.argv[1:] + lines))


if __name__ == "__main__":
    main()
