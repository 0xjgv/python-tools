# pseudo code
# https://docs.google.com/spreadsheets/d/1o68XX6yUDt5C70EaikV2ViIwLvslKU5Ct8bYqq82yPQ/edit#gid=0


def scramble_emails(domain: str, usernames: [str]) -> [str]:
    """
    Scramble usernames & append domain
    TODO: add logic to scramble emails
    """
    for user in usernames:
        if "@" in user:
            yield user
        else:
            yield f"{user}@{domain}"
