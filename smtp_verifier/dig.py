from json import load, dump
from os import popen
from smtp_verifier.config import MX_DOMAINS_PATH


def mx_domains_middleware(fn):
    mx_by_domain = {}
    if MX_DOMAINS_PATH.exists():
        with MX_DOMAINS_PATH.open("r") as file:
            mx_by_domain = load(file) or {}

    def wrapper(domain):
        # here: invalidate cache
        if domain not in mx_by_domain:
            mx_by_domain[domain] = fn(domain)
            try:
                with MX_DOMAINS_PATH.open("w") as file:
                    dump(mx_by_domain, file)
            except Exception as exc:
                print(exc)
        return mx_by_domain.get(domain)

    return wrapper


@mx_domains_middleware
def get_mx_servers(domain) -> list[dict]:
    print(f"Getting MX servers for {domain}...")
    results = popen(f"dig +short mx {domain}").read()
    mxs = []
    for line in results.splitlines():
        if line[0].isnumeric():
            priority, mx = line.split(" ")
            mxs.append((priority, mx[:-1]))
    return [v for _, v in sorted(mxs, key=lambda x: int(x[0]))]


# from asyncio import gather, create_subprocess_shell, subprocess
# from urllib.parse import urlparse

# async def get_mx_servers_async(url: str) -> dict:
#     domain = urlparse(url).hostname
#     if not domain:
#         domain = url
#     print(f"Getting MX servers for {domain}...")

#     proc = await create_subprocess_shell(
#         f"dig +short mx {domain}",
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
#     stdout, stderr = await proc.communicate()

#     mxs = []
#     if stderr:
#         print("Something went wrong", stderr)
#         return {domain: mxs}

#     for line in stdout.decode("utf8").splitlines():
#         if line[0].isnumeric():
#             priority, mx = line.split(" ")
#             mxs.append((priority, mx[:-1]))

#     return [v for _, v in sorted(mxs, key=lambda x: int(x[0]))]


# async def get_all_mxs_async(domains):
#     return await gather(*(get_mx_servers(domain) for domain in domains))


if __name__ == "__main__":
    res = get_mx_servers("onerpm.com")
    print("Res", res)
