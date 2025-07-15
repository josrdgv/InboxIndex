import json
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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
    except Exception as e:
        continue

    for topic in email.get("topics", []):
        topic_counts[topic][month] += 1

# Prepare data
all_months = sorted(set(m for topic in topic_counts for m in topic_counts[topic]))
topics = list(topic_counts.keys())

# Build a dict of cumulative topic values
topic_series = {t: [topic_counts[t].get(m, 0) for m in all_months] for t in topics}

# Initialize plot
fig, ax = plt.subplots(figsize=(12, 6))
lines = {t: ax.plot([], [], label=t)[0] for t in topics}

def init():
    ax.set_xlim(0, len(all_months))
    ax.set_ylim(0, max(max(v) for v in topic_series.values()) + 5)
    ax.set_title("Enron Email Topics Over Time (Animated)", fontsize=16)
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Emails")
    ax.set_xticks(range(len(all_months)))
    ax.set_xticklabels(all_months, rotation=45, fontsize=8)
    ax.grid(True)
    return list(lines.values())

def update(frame):
    for t in topics:
        lines[t].set_data(range(frame+1), topic_series[t][:frame+1])
    return list(lines.values())

ani = FuncAnimation(fig, update, frames=len(all_months), init_func=init, blit=True, interval=300)

# Save animation as mp4
output_path = "static/story-insight.mp4"
ani.save(output_path, writer="ffmpeg")

plt.legend()
plt.tight_layout()
print(f"🎬 Animation saved to {output_path}")
