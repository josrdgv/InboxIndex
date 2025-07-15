from flask import Flask, render_template, request
import json
from datetime import datetime
from collections import defaultdict
import plotly.graph_objs as go
import plotly.offline as pyo

app = Flask(__name__)

# Load parsed email data
with open("parsed_emails.json", "r", encoding="utf-8") as f:
    ALL_EMAILS = json.load(f)

EMAILS_PER_PAGE = 10

def paginate(emails, page):
    start = (page - 1) * EMAILS_PER_PAGE
    end = start + EMAILS_PER_PAGE
    return emails[start:end]

def filter_emails(query):
    query = query.lower()
    return [email for email in ALL_EMAILS if query in email.get("from", "").lower()
                                           or query in email.get("to", "").lower()
                                           or query in email.get("subject", "").lower()]

def generate_topic_chart(filtered_emails):
    topic_counts = defaultdict(lambda: defaultdict(int))

    for email in filtered_emails:
        date_str = email.get("date", "")
        try:
            date = datetime.strptime(date_str[:16], "%a, %d %b %Y")
            month = date.strftime("%Y-%m")
        except:
            continue

        for topic in email.get("topics", []):
            topic_counts[topic][month] += 1

    all_months = sorted({m for t in topic_counts for m in topic_counts[t]})
    data = []
    for topic, counts in topic_counts.items():
        y = [counts.get(m, 0) for m in all_months]
        trace = go.Bar(x=all_months, y=y, name=topic)
        data.append(trace)

    layout = go.Layout(title="Email Topics Over Time (Bar Chart)",
                       xaxis=dict(title="Month"),
                       yaxis=dict(title="Email Count"),
                       barmode='group',
                       margin=dict(l=40, r=40, t=50, b=120))

    fig = go.Figure(data=data, layout=layout)
    chart_html = pyo.plot(fig, output_type='div', include_plotlyjs=False)
    return chart_html

@app.route("/")
def home():
    page = int(request.args.get("page", 1))
    total_pages = (len(ALL_EMAILS) - 1) // EMAILS_PER_PAGE + 1
    paged_emails = paginate(ALL_EMAILS, page)
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    return render_template(
        "index.html",
        emails=paged_emails,
        search_query="",
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        chart_div=None
    )

@app.route("/search")
def search():
    query = request.args.get("query", "").strip().lower()
    page = int(request.args.get("page", 1))

    if not query:
        return home()

    filtered = filter_emails(query)
    total_pages = (len(filtered) - 1) // EMAILS_PER_PAGE + 1
    paged_emails = paginate(filtered, page)
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    chart_div = generate_topic_chart(filtered) if filtered else None

    return render_template(
        "index.html",
        emails=paged_emails,
        search_query=query,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        chart_div=chart_div
    )

@app.route("/topic/<topic_name>")
def topic_filter(topic_name):
    topic_name = topic_name.lower()
    filtered = [
        email for email in ALL_EMAILS
        if topic_name in [t.lower() for t in email.get("topics", [])]
    ]

    page = int(request.args.get("page", 1))
    total_pages = (len(filtered) - 1) // EMAILS_PER_PAGE + 1
    paged_emails = paginate(filtered, page)

    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    chart_div = generate_topic_chart(filtered) if filtered else None

    return render_template(
        "index.html",
        emails=paged_emails,
        search_query=f"Topic: {topic_name}",
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        chart_div=chart_div
    )

if __name__ == "__main__":
    app.run(debug=True)
