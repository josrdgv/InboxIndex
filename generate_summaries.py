import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_text(text, max_chunk_words=1000):
    try:
        words = text.split()
        if len(words) <= max_chunk_words:
            chunks = [text]
        else:
            chunks = [" ".join(words[i:i + max_chunk_words]) for i in range(0, len(words), max_chunk_words)]

        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes emails."},
                    {"role": "user", "content": f"Summarize the following chunk of an email:\n{chunk}"}
                ],
                temperature=0.5,
                max_tokens=200
            )
            summary = response.choices[0].message.content.strip()
            chunk_summaries.append(summary)

        combined = " ".join(chunk_summaries)

        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize combined summaries into one concise version."},
                {"role": "user", "content": f"Summarize the following combined summaries:\n{combined}"}
            ],
            temperature=0.5,
            max_tokens=150
        )
        return final_response.choices[0].message.content.strip()

    except Exception as e:
        print("\u26a0\ufe0f Summarization error:", e)
        return ""


# Load emails
with open("parsed_emails.json", "r", encoding="utf-8") as f:
    emails = json.load(f)

# Summarize and update
for email in emails:
    if "summary" not in email or not email["summary"]:
        body = email.get("body", "")
        if body and len(body.split()) > 30:
            email["summary"] = summarize_text(body)
        else:
            email["summary"] = ""

# Save updated JSON
with open("parsed_emails.json", "w", encoding="utf-8") as f:
    json.dump(emails, f, indent=2)

print("\u2705 Summaries updated in parsed_emails.json")
