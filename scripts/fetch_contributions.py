import json, re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = "vijay711-github"
URL = f"https://github.com/users/{USERNAME}/contributions"
html = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

days = []
for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    count = cell.get("data-count")
    level = cell.get("data-level")
    if date:
        days.append({
            "date": date,
            "count": int(count or 0),
            "level": int(level or 0)
        })

days = days[-371:]
total = sum(d["count"] for d in days)
best = max(days, key=lambda d: d["count"], default={"count": 0, "date": ""})

data = {
    "username": USERNAME,
    "days": days,
    "total": total,
    "best_day": best,
}

output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

(output_dir / "contributions.json").write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)
Path("data/contributions.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"Saved {len(days)} days, {total} contributions.")
