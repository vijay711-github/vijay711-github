import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "vijay711-github"

url = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    url,
    timeout=30,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

response.raise_for_status()

html = response.text
soup = BeautifulSoup(html, "html.parser")

days = []

# GitHub contribution cells
for cell in soup.select("td.ContributionCalendar-day"):

    date = cell.get("data-date")

    # GitHub can expose the contribution number in
    # aria-label, data-count, or title depending on the page version.
    text = " ".join(cell.stripped_strings)

    aria = cell.get("aria-label", "")
    data_count = cell.get("data-count", "")

    combined = f"{aria} {text} {data_count}"

    match = re.search(
        r"([\d,]+)\s+contributions?",
        combined,
        re.IGNORECASE
    )

    if match:
        count = int(match.group(1).replace(",", ""))
    else:
        count = 0

    level = cell.get("data-level", "0")

    try:
        level = int(level)
    except ValueError:
        level = 0

    days.append({
        "date": date,
        "count": count,
        "level": level
    })


# ---------------------------------------------------------
# Get the total directly from GitHub's contribution heading
# ---------------------------------------------------------

total = None

patterns = [
    r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year",
    r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year",
]

for pattern in patterns:

    match = re.search(
        pattern,
        html,
        re.IGNORECASE
    )

    if match:
        total = int(
            match.group(1).replace(",", "")
        )
        break


# If GitHub doesn't expose the heading, calculate it.
if total is None:
    total = sum(
        day["count"]
        for day in days
    )


# Keep the latest year of cells
days = days[-371:]


best_day = max(
    days,
    key=lambda day: day["count"],
    default={
        "date": "",
        "count": 0,
        "level": 0
    }
)


data = {
    "username": USERNAME,
    "days": days,
    "total": total,
    "best_day": best_day
}


# Make sure data directory exists
output_dir = Path("data")
output_dir.mkdir(
    parents=True,
    exist_ok=True
)


output_file = output_dir / "contributions.json"

output_file.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)


print("=" * 50)
print("GitHub Contribution Fetch")
print("=" * 50)
print(f"Username: {USERNAME}")
print(f"Days found: {len(days)}")
print(f"Total contributions: {total}")
print(
    f"Best day: {best_day['date']} "
    f"({best_day['count']} contributions)"
)
print("=" * 50)
