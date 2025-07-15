import json

def categorize_topics(text):
    keywords = {
        "Regulatory": ["ferc", "compliance", "regulation", "oversight"],
        "Finance": ["bonus", "salary", "finance", "deal", "merger", "transaction"],
        "Legal": ["lawsuit", "contract", "agreement", "legal", "settlement"],
        "HR": ["employee", "vacation", "hiring", "hr", "leave"]
    }
    text = text.lower()
    return [label for label, keys in keywords.items() if any(k in text for k in keys)]

with open("parsed_emails.json", "r", encoding="utf-8") as f:
    emails = json.load(f)

for email in emails:
    combined_text = f"{email.get('subject', '')} {email.get('body', '')}"
    email["topics"] = categorize_topics(combined_text)

with open("parsed_emails.json", "w", encoding="utf-8") as f:
    json.dump(emails, f, indent=2)

print("✅ Topics added to parsed_emails.json")
