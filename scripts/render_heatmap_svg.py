import json
from pathlib import Path

data_path = Path("data/contributions.json")
if not data_path.exists():
    raise SystemExit("Missing data/contributions.json. Run scripts/fetch_contributions.py first.")

data = json.loads(data_path.read_text(encoding="utf-8"))
days = data.get("days", [])[-371:]
if not days:
    raise SystemExit("No contribution days found in data/contributions.json; check the fetch script output.")

days = [{"count": 0, "level": 0}] * (371 - len(days)) + days
counts = [int(d.get("count", 0) or 0) for d in days]
max_count = max(counts) if counts else 0
palette = ["#172033", "#14532d", "#15803d", "#16a34a", "#4ade80"]
total = data.get("total", sum(counts))

parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="190" viewBox="0 0 1000 190">',
    '<rect width="1000" height="190" rx="18" fill="#0b1220" stroke="#263449"/>',
    f'<text x="28" y="35" font-family="monospace" font-size="15" fill="#a7f3d0">GITHUB CONTRIBUTION ACTIVITY · {int(total):,} CONTRIBUTIONS</text>',
    '<text x="28" y="57" font-family="monospace" font-size="12" fill="#94a3b8">Fetched from GitHub contribution data · refreshed by Actions</text>',
]
for i, day in enumerate(days):
    col, row = divmod(i, 7)
    x, y = 28 + col * 17, 75 + row * 13
    count = int(day.get("count", 0) or 0)
    if count <= 0 or max_count <= 0:
        level = 0
    elif count / max_count <= .25:
        level = 1
    elif count / max_count <= .5:
        level = 2
    elif count / max_count <= .75:
        level = 3
    else:
        level = 4
    parts.append(f'<rect x="{x}" y="{y}" width="11" height="9" rx="2" fill="{palette[level]}" stroke="#263449" stroke-width=".35"><title>{count} contributions</title></rect>')
parts.extend([
    '<text x="28" y="174" font-family="monospace" font-size="11" fill="#64748b">LESS</text>',
    '<text x="925" y="174" font-family="monospace" font-size="11" fill="#64748b">MORE</text>',
    '</svg>'
])
Path("assets/contrib-heatmap.svg").write_text("\\n".join(parts), encoding="utf-8")
