import json
from enron_analysis import parse_all_emails

emails = parse_all_emails()  # no limit!
with open("parsed_emails.json", "w", encoding="utf-8") as f:
    json.dump(emails, f, indent=2)
