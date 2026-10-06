import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "vijay711-github"

URL = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    URL,
    timeout=30,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):

    date = cell.get("data-date")

    # GitHub may not expose data-count anymore.
    # Read the number from aria-label instead.
    aria_label = cell.get("aria-label", "")

    count = 0

    match = re.search(r"([\d,]+)\s+contributions?", aria_label)

    if match:
        count = int(match.group(1).replace(",", ""))

    # Keep data-level if available.
    level = cell.get("data-level")

    if level is None:
        level = 0

    days.append({
        "date": date,
        "count": count,
        "level": int(level)
    })


# Last 365/371 days
days = days[-371:]

total = sum(day["count"] for day in days)

best_day = max(
    days,
    key=lambda day: day["count"],
    default={
        "count": 0,
        "date": ""
    }
)


data = {
    "username": USERNAME,
    "days": days,
    "total": total,
    "best_day": best_day
}


# Make sure the data directory exists
output_dir = Path("data")
output_dir.mkdir(
    parents=True,
    exist_ok=True
)


(output_dir / "contributions.json").write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)


print(f"Saved {len(days)} days.")
print(f"Total contributions: {total}")
print(
    f"Best day: {best_day['date']} "
    f"({best_day['count']} contributions)"
)
