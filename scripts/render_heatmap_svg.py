import json
from pathlib import Path

data = json.loads(Path("data/contributions.json").read_text(encoding="utf-8"))
days = data.get("days", [])
palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

# Normalize to 53 weeks x 7 days. Pad at the beginning.
days = days[-371:]
days = [{"date": "", "count": 0, "level": 0}] * (371-len(days)) + days

w, h = 900, 190
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
    '<rect width="900" height="190" rx="16" fill="#0d1117" stroke="#30363d"/>',
    f'<text x="30" y="34" fill="#8b949e" font-family="monospace" font-size="15">{data.get("total",0):,} contributions in the last year</text>'
]
for i, d in enumerate(days):
    col, row = divmod(i, 7)
    x, y = 30 + col*14, 55 + row*14
    level = max(0, min(4, int(d.get("level",0))))
    delay = (col * 0.025 + row * 0.008)
    parts.append(
        f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{palette[level]}">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay:.3f}s" fill="freeze"/></rect>'
    )
parts += [
    '<text x="30" y="170" fill="#8b949e" font-family="monospace" font-size="13">Less</text>',
    '<text x="650" y="170" fill="#8b949e" font-family="monospace" font-size="13">More</text>',
]
for i, color in enumerate(palette):
    parts.append(f'<rect x="{70+i*16}" y="160" width="10" height="10" rx="2" fill="{color}"/>')
parts.append("</svg>")
Path("profile/contrib-heatmap.svg").write_text("\n".join(parts), encoding="utf-8")
