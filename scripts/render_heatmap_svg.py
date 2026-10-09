
import json
from pathlib import Path

data_path = Path("data/contributions.json")
output_path = Path("assets/contrib-heatmap.svg")

if not data_path.exists():
    raise SystemExit("Missing data/contributions.json")

data = json.loads(data_path.read_text(encoding="utf-8"))
days = data.get("days", [])[-371:]

if not days:
    raise SystemExit("No contribution days found")

# GitHub's fetched levels are usable even when count parsing fails.
palette = ["#172033", "#0e4429", "#006d32", "#26a641", "#39d353"]

def get_level(day):
    count = int(day.get("count", 0) or 0)

    if count > 0:
        return min(4, max(1, int(day.get("level", 0) or 0),
                          min(4, count)))
    
    # Fall back to GitHub's actual contribution intensity.
    try:
        return min(4, max(0, int(day.get("level", 0) or 0)))
    except (ValueError, TypeError):
        return 0

# Pad to a full year of 371 cells.
days = [{"count": 0, "level": 0}] * (371 - len(days)) + days
total = int(data.get("total", 0) or 0)

parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="1000" height="190" viewBox="0 0 1000 190">',
    '<rect width="1000" height="190" rx="18" '
    'fill="#0b1220" stroke="#263449"/>',
    f'<text x="28" y="35" font-family="monospace" '
    f'font-size="15" fill="#a7f3d0">'
    f'GITHUB CONTRIBUTION ACTIVITY · {total:,} CONTRIBUTIONS</text>',
    '<text x="28" y="57" font-family="monospace" '
    'font-size="12" fill="#94a3b8">'
    'GitHub contribution intensity · refreshed by Actions</text>',
]

# The fetched HTML is ordered by weekday, then by week.
for i, day in enumerate(days):
    row = i // 53
    col = i % 53

    x = 28 + col * 17
    y = 75 + row * 13
    level = get_level(day)
    count = int(day.get("count", 0) or 0)
    date = day.get("date", "Unknown date")

    tooltip = (
        f"{date}: {count} contributions"
        if count > 0
        else f"{date}: contribution intensity level {level}"
    )

    tooltip = (
        tooltip.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    parts.append(
        f'<rect x="{x}" y="{y}" width="11" height="9" rx="2" '
        f'fill="{palette[level]}" stroke="#263449" stroke-width=".35">'
        f'<title>{tooltip}</title></rect>'
    )

parts.extend([
    '<text x="28" y="174" font-family="monospace" '
    'font-size="11" fill="#64748b">LESS</text>',
    '<text x="925" y="174" font-family="monospace" '
    'font-size="11" fill="#64748b">MORE</text>',
    '</svg>'
])

output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text("\n".join(parts), encoding="utf-8")

print(f"Rendered {len(days)} cells; total contributions: {total}")
print(f"Output: {output_path}")
