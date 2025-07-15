import json
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from dateutil.parser import parse
import os

# Load parsed email data
with open("parsed_emails.json", "r", encoding="utf-8") as f:
    emails = json.load(f)

# Count topics per month
topic_counts = defaultdict(lambda: defaultdict(int))

for email in emails:
    date_str = email.get("date", "")
    try:
        date = parse(date_str, fuzzy=True)
        month = date.strftime("%Y-%m")
    except Exception:
        continue

    for topic in email.get("topics", []):
        topic_counts[topic][month] += 1

# Prepare plot
plt.figure(figsize=(10, 4))

all_months = sorted(set(m for t in topic_counts for m in topic_counts[t]))
topics = list(topic_counts.keys())

for topic in topics:
    values = [topic_counts[topic].get(m, 0) for m in all_months]
    plt.plot(all_months, values, label=topic, linewidth=2)

plt.title("Email Topics Over Time", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Count")
plt.xticks(rotation=45, fontsize=8)
plt.yticks(fontsize=8)
plt.grid(True, linestyle="--", alpha=0.3)
plt.legend(fontsize=8)
plt.tight_layout()

# Save with transparent background
plt.savefig("static/story-insight.png", transparent=True)
print("✅ Chart saved with transparent background")
