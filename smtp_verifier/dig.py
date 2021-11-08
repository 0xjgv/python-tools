from asyncio import gather, create_subprocess_shell, subprocess
from os.path import exists, dirname
from urllib.parse import urlparse
from json import load, dump
from pathlib import Path
from os import popen


MX_DOMAINS_PATH = "./cache/mx_by_domain.json"


def mx_domains_middleware(fn):
    mx_by_domain = {}
    if exists(MX_DOMAINS_PATH):
        with open(MX_DOMAINS_PATH, "r") as file:
            mx_by_domain = load(file)
    else:
        Path(dirname(MX_DOMAINS_PATH)).mkdir(parents=True, exist_ok=True)

    def wrapper(domain):
        if domain not in mx_by_domain:
            mx_by_domain[domain] = fn(domain)
            try:
                with open(MX_DOMAINS_PATH, "w") as file:
                    dump(mx_by_domain, file)
            except Exception as exc:
                print(exc)
        return mx_by_domain.get(domain)

    return wrapper


@mx_domains_middleware
def get_mx_servers(domain):
    print(f"Getting MX servers for {domain}...")
    results = popen(f"dig +short mx {domain}").read()
    mxs = []
    for line in results.splitlines():
        if line[0].isnumeric():
            priority, mx = line.split(" ")
            mxs.append((priority, mx[:-1]))
    return [v for _, v in sorted(mxs, key=lambda x: int(x[0]))]


async def get_mx_servers_async(url: str) -> dict:
    domain = urlparse(url).hostname
    if not domain:
        domain = url
    print(f"Getting MX servers for {domain}...")

    proc = await create_subprocess_shell(
        f"dig +short mx {domain}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    mxs = []
    if stderr:
        print("Something went wrong", stderr)
        return {domain: mxs}

    for line in stdout.decode("utf8").splitlines():
        if line[0].isnumeric():
            priority, mx = line.split(" ")
            mxs.append((priority, mx[:-1]))

    return [v for _, v in sorted(mxs, key=lambda x: int(x[0]))]


async def get_all_mxs_async(domains):
    return await gather(*(get_mx_servers(domain) for domain in domains))


if __name__ == "__main__":
    res = get_mx_servers("onerpm.com")
    print("Res", res)
