import json
from pathlib import Path

data=json.loads(Path("data/contributions.json").read_text(encoding="utf-8"))
days=data.get("days",[])[-371:]
days=[{"count":0,"level":0} for _ in range(371-len(days))]+days
pal=["#172033","#12352c","#12614b","#16a36a","#4ade80"]
total=data.get("total",0)
out=[
'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="190" viewBox="0 0 900 190">',
'<rect width="900" height="190" rx="18" fill="#0b1220" stroke="#263244"/>',
f'<text x="30" y="35" fill="#dbeafe" font-family="ui-monospace,monospace" font-size="16" font-weight="700">GitHub activity · {total:,} contributions</text>',
'<text x="30" y="58" fill="#64748b" font-family="ui-monospace,monospace" font-size="12">Updated automatically from GitHub</text>']
for i,d in enumerate(days):
    col,row=divmod(i,7)
    x,y=30+col*14,78+row*14
    level=max(0,min(4,int(d.get("level",0))))
    delay=col*.02+row*.006
    out.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="3" fill="{pal[level]}"><animate attributeName="opacity" from="0" to="1" dur=".35s" begin="{delay:.3f}s" fill="freeze"/></rect>')
out += ['<text x="30" y="178" fill="#64748b" font-family="ui-monospace,monospace" font-size="11">Less</text>','<text x="825" y="178" fill="#64748b" font-family="ui-monospace,monospace" font-size="11">More</text>','</svg>']
Path("assets/contrib-heatmap.svg").write_text("\n".join(out),encoding="utf-8")
