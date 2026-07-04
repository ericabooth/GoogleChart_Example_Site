#!/usr/bin/env python3
"""Generate authentic googlechart HTML output WITHOUT Stata, by reproducing
googlechart_writehtml.ado's page shell and inlining the real engine JS
(googlechart_engine.sthlp).  Produces one self-contained HTML per chart plus
a hand-built, annotated index.html landing page for GitHub Pages.

Data: 2025 County Health Rankings state-level extract (../data/chr_states_2025.csv).
"""
import os, json, csv, html

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.dirname(HERE)
DATA   = os.path.join(ROOT, "data", "chr_states_2025.csv")
ENGINE = os.path.join(ROOT, "package_files", "googlechart", "googlechart_engine.sthlp")
CHARTS = os.path.join(HERE, "charts")
os.makedirs(CHARTS, exist_ok=True)

with open(ENGINE, encoding="utf-8") as f:
    ENGINE_JS = f.read()

# ---- CSS block, transcribed from googlechart_writehtml.ado (tx2036 on) ------
CSS = r""":root{--ink:#1B2D55;--accent:#D44500;--link:#2B6CB0;--bg:#F5F7FA;--muted:#6C7A8D;--card:#ffffff;--line:#e2e8f0;}
*{box-sizing:border-box;}body{margin:0;font-family:'Montserrat',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--ink);font-weight:400;letter-spacing:-0.005em;}
h1{font-weight:700;letter-spacing:-0.01em;}
.controls h3{font-weight:600;}
.wrap{max-width:1180px;margin:0 auto;padding:24px 18px 48px;}
h1{font-size:1.5rem;margin:0 0 4px;color:var(--ink);}
.sub{color:var(--muted);margin:0 0 16px;font-size:.95rem;}
.panels{display:grid;grid-template-columns:240px 1fr;gap:18px;align-items:start;}
@media (max-width:780px){.panels{grid-template-columns:1fr;}}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;box-shadow:0 1px 2px rgba(15,23,42,.05);}
.controls h3{font-size:.78rem;text-transform:uppercase;letter-spacing:.05em;margin:8px 0 6px;color:var(--muted);}
.controls label{display:block;font-size:.85rem;margin:8px 0 2px;color:var(--ink);font-weight:500;}
.controls button{width:100%;padding:6px 8px;font-size:.85rem;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink);cursor:pointer;}
.controls button:hover{background:#eef2f7;}
.chartcard{padding:14px;min-height:100px;}
.meta{font-size:.78rem;color:var(--muted);margin-top:10px;}
.note{margin-top:14px;color:var(--muted);font-size:.78rem;}
.exportmenu{position:relative;}
.exportbtn{width:100%;padding:6px 8px;font-size:.85rem;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink);cursor:pointer;text-align:left;}
.exportbtn:hover{background:#eef2f7;}
.exportlist{position:absolute;top:calc(100% + 4px);left:0;right:0;background:#fff;border:1px solid var(--line);border-radius:6px;box-shadow:0 4px 12px rgba(15,23,42,.12);z-index:40;display:flex;flex-direction:column;padding:4px;}
.exportlist button{width:100%;padding:6px 8px;font-size:.85rem;border:none;border-radius:4px;background:none;color:var(--ink);cursor:pointer;text-align:left;}
.exportlist button:hover{background:#eef2f7;}
#chart-footer{display:none;justify-content:flex-end;align-items:center;gap:8px;padding:8px 0 0;border-top:1px solid var(--line);margin-top:8px;}
#chart-footer.active{display:flex;}
#chart-footer button{padding:4px 10px;font-size:.8rem;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink);cursor:pointer;}
#chart-footer button:hover{background:#eef2f7;}
#chart-footer .exportmenu{position:relative;}
#chart-footer .exportlist{left:auto;right:0;min-width:170px;}
.panels.no-sidebar{grid-template-columns:1fr !important;}
.controls.empty{display:none;}
.gc-filters{display:flex;flex-direction:column;gap:6px;margin-bottom:8px;align-items:flex-start;}
.gc-filter-slot{min-height:34px;}
.gc-filters label{display:block;font-size:.78rem;color:var(--muted);font-weight:500;margin-top:6px;}
.gc-play{align-self:flex-start;width:auto;padding:5px 14px;font-size:.85rem;border:1px solid var(--link);border-radius:6px;background:var(--ink);color:#fff;cursor:pointer;font-weight:500;}
.gc-play:hover{background:var(--link);}
#datatable{display:none;margin-top:14px;border:1px solid var(--line);border-radius:8px;background:#fff;}
#datatable.open{display:block;}
#datatable .dt-header{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-bottom:1px solid var(--line);background:#f8fafc;border-radius:8px 8px 0 0;font-size:.9rem;}
#datatable .dt-count{color:var(--muted);font-size:.8rem;font-weight:normal;margin-left:8px;}
#datatable .dt-close{background:none;border:none;font-size:1.3rem;line-height:1;cursor:pointer;color:var(--muted);padding:0 4px;}
#datatable .dt-scroll{max-height:360px;overflow:auto;}
#datatable table.dt-table{width:100%;border-collapse:collapse;font-size:.8rem;}
#datatable .dt-table th{position:sticky;top:0;background:#fff;border-bottom:1px solid var(--line);padding:6px 10px;text-align:left;font-weight:600;color:var(--ink);white-space:nowrap;}
#datatable .dt-table td{padding:5px 10px;border-bottom:1px solid #f1f5f9;color:#334155;}
#datatable .dt-table tr:hover td{background:#f8fafc;}
#datatable .dt-truncated{padding:8px 12px;border-top:1px solid var(--line);color:var(--muted);font-size:.78rem;background:#f8fafc;border-radius:0 0 8px 8px;}
@media print {.controls{display:none !important;}#datatable{display:none !important;}.panels{grid-template-columns:1fr !important;}body{background:#fff;}}
.gc-type-pie .panels, .gc-type-donut .panels { grid-template-columns: 240px max-content; justify-content: start; }
.gc-type-pie .chartcard, .gc-type-donut .chartcard { width: max-content; max-width: 100%; }
@media (max-width:780px){.gc-type-pie .panels,.gc-type-donut .panels{grid-template-columns:1fr;}.gc-type-pie .chartcard,.gc-type-donut .chartcard{width:auto;}}
.gc-type-timeline #chart { overflow-x: auto; overflow-y: hidden; }
.gc-type-timeline .chartcard { overflow: hidden; }
.gc-type-table .chartcard { min-width: 0; max-width: 100%; overflow: hidden; }
.gc-type-table #chart { overflow: hidden; min-width: 0; width: 100%; }
.gc-table-wrap { border-radius: 8px; overflow: hidden; border: 1px solid var(--line); }
.gc-table-search { display: flex; gap: 8px; padding: 8px 12px; background:#f8fafc; border-bottom:1px solid var(--line); align-items:center;}
.gc-table-search input { flex: 1; padding: 6px 10px; font-size: .88rem; border: 1px solid var(--line); border-radius: 6px; outline: none; }
.gc-table-search input:focus { border-color: var(--link); box-shadow: 0 0 0 2px rgba(43,108,176,.15); }
.gc-table-search .count { color: var(--muted); font-size: .78rem; white-space: nowrap; }
.gc-table-wrap { overflow-x: auto; max-width: 100%; }
.gc-table-wrap > div:not(.gc-table-search) { display: block; min-width: max-content; }
.google-visualization-table-table { border-collapse: collapse !important; font-family: 'Montserrat',-apple-system,sans-serif !important; font-size: .85rem !important; width: auto !important; min-width: 100% !important; }
.google-visualization-table-table th, .google-visualization-table-table td { white-space: nowrap !important; min-width: 180px !important; padding: 8px 12px !important; }
.google-visualization-table-table th:first-child, .google-visualization-table-table td:first-child { min-width: 260px !important; }
.google-visualization-table-table th { position: sticky; top: 0; background: var(--ink) !important; color: #fff !important; padding: 8px 10px !important; font-weight: 600 !important; text-align: left !important; border-bottom: 1px solid var(--line) !important; }
.google-visualization-table-table td { padding: 6px 10px !important; border-bottom: 1px solid #f1f5f9 !important; color: #1B2D55 !important; vertical-align: top !important; }
.google-visualization-table-table tr.google-visualization-table-tr-even td { background: #ffffff !important; }
.google-visualization-table-table tr.google-visualization-table-tr-odd  td { background: #f8fafc !important; }
.google-visualization-table-table tr.google-visualization-table-tr-over td { background: #eef2f7 !important; }
.google-visualization-table-table td.gc-num { font-variant-numeric: tabular-nums; text-align: right; font-feature-settings:'tnum'; }
.google-visualization-table-page-numbers { padding: 8px 12px !important; background:#f8fafc !important; border-top:1px solid var(--line) !important; }"""

META_DEFAULTS = dict(
    type="", scheme="tx2036", width=980, height=644, title="", subtitle="", note="",
    xvar="value", yvar="", xlabel="", ylabel="", name="", over="", level="", time="",
    namelabel="", valuelabel="", levelorder="", centerlevel="",
    download=1, datatable=1, animate=1, tx2036style=1, downloadpos="below",
    stacked=0, normalize=0, directlabels=0, innerradius=0.45, bucketsize=0,
    geo_region="", geo_resolution="", combo_types="", combo_default="",
    labelwrap="auto", legendpos="", table_search=0, table_sticky=0, table_frozencols=0,
)

def make_html(meta, data, filters=None):
    m = dict(META_DEFAULTS); m.update(meta)
    filters = filters or []
    esc_title = html.escape(m["title"])
    parts = []
    w = parts.append
    w('<!DOCTYPE html>')
    w('<html lang="en"><head>')
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w(f'<title>{esc_title}</title>')
    w('<link rel="preconnect" href="https://fonts.googleapis.com">')
    w('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    w('<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">')
    w('<script src="https://www.gstatic.com/charts/loader.js"></script>')
    w('<style>')
    w(CSS)
    w('</style>')
    w(f'</head><body class="gc-type-{m["type"].lower()}">')
    w('<div class="wrap">')
    w(f'<h1>{esc_title}</h1>')
    if m["subtitle"]:
        w(f'<p class="sub">{html.escape(m["subtitle"])}</p>')
    w('<div class="panels">')
    w('  <div class="card controls" id="controls"></div>')
    w('  <div class="card chartcard"><div id="chart"></div><div id="chart-footer"></div></div>')
    w('</div>')
    w('<div id="datatable"></div>')
    if m["note"]:
        w(f'<p class="note">{html.escape(m["note"])}</p>')
    w('</div>')
    payload = {"meta": m, "filters": filters, "data": data}
    w('<script>')
    w('window.__GOOGLECHART__ = ' + json.dumps(payload) + ';')
    w('</script>')
    w('<script>')
    w(ENGINE_JS)
    w('</script>')
    w('<script>googlechartRender(window.__GOOGLECHART__);</script>')
    w('</body></html>')
    return "\n".join(parts)

# ---- Load data --------------------------------------------------------------
rows = list(csv.DictReader(open(DATA)))
for r in rows:
    for k in ("median_income","premature_death","obesity","uninsured",
              "child_poverty","unemployment","pct_rural"):
        r[k] = float(r[k])

SRC = ("Source: County Health Rankings & Roadmaps 2025 (University of Wisconsin "
       "Population Health Institute). Requires internet at view time (Google Charts CDN).")

def num(x):  # keep ints tidy
    return int(x) if float(x).is_integer() else round(float(x), 1)

built = []
def build(fname, meta, data, filters=None):
    open(os.path.join(CHARTS, fname), "w", encoding="utf-8").write(make_html(meta, data, filters))
    built.append(fname)

# (1) GEO -- uninsured by state
build("01_geo_uninsured.html",
      dict(type="geo", name="geo_code", geo_region="US", geo_resolution="us-states",
           scheme="blues", width=960, height=560,
           title="Uninsured rate by state, 2025",
           note=SRC),
      [{"value": num(r["uninsured"]), "name": r["geo_code"]} for r in rows])

# (2) BAR -- 15 highest-uninsured states.
# NOTE: animate is deliberately OFF here.  Google Charts throws when
# animation.startup is combined with the annotation-role DataView that
# directlabels builds for a BarChart, which leaves the chart blank.  The
# package's own tested bar recipe omits animate for the same reason.
top = sorted(rows, key=lambda r: -r["uninsured"])[:15]
build("02_bar_uninsured.html",
      dict(type="bar", name="usps", directlabels=1, animate=0, width=900, height=560,
           title="Fifteen states with the highest uninsured rate, 2025",
           xlabel="Uninsured (%)", note=SRC),
      [{"value": num(r["uninsured"]), "name": r["usps"]} for r in top])

# (3) SCATTER -- income vs premature death
build("03_scatter_income_ypll.html",
      dict(type="scatter", name="state", xvar="median_income", yvar="premature_death",
           width=920, height=560,
           title="Median income vs premature death (states, 2025)",
           xlabel="Median household income (USD)",
           ylabel="Premature death (YPLL per 100,000)", note=SRC),
      [{"x": num(r["median_income"]), "y": num(r["premature_death"]),
        "name": r["state"], "t__uninsured": num(r["uninsured"]),
        "t__child_poverty": num(r["child_poverty"])} for r in rows])

# (4) BUBBLE -- child poverty vs premature death, size=rural, color=uninsured band,
#     animated across a real 2024->2025 panel via a Play button (time=year).
panel = list(csv.DictReader(open(os.path.join(ROOT, "data", "chr_states_panel.csv"))))
for r in panel:
    for k in ("child_poverty","premature_death","pct_rural","uninsured"):
        r[k] = float(r[k])
    r["year"] = int(r["year"])
build("04_bubble.html",
      dict(type="bubble", name="usps", over="highunins", time="year",
           xvar="child_poverty", yvar="premature_death", width=920, height=560,
           title="Child poverty vs premature death (press Play: 2016 to 2025)",
           subtitle="Bubble size = rural share; color = uninsured band. Use Play/slider to animate across years.",
           xlabel="Children in poverty (%)",
           ylabel="Premature death (YPLL per 100,000)",
           note="2024 and 2025 are actual County Health Rankings releases; "
                "2016-2023 are a simulated trajectory included only to demonstrate "
                "the Play/time-slider control. Requires internet at view time."),
      [{"x": num(r["child_poverty"]), "y": num(r["premature_death"]),
        "size": num(r["pct_rural"]),
        "g": "Uninsured >= 10%" if r["uninsured"] >= 10 else "Uninsured < 10%",
        "name": r["usps"], "t": r["year"],
        "t__uninsured": num(r["uninsured"])} for r in panel])

# (5) TABLE -- searchable, sticky header
tvars = ["state","uninsured","median_income","premature_death","obesity",
         "child_poverty","unemployment","pct_rural"]
build("05_table.html",
      dict(type="table", table_search=1, table_sticky=1, width=980, height=460,
           title="2025 County Health Rankings: state measures (searchable)",
           note=SRC),
      [{"_": None, **{f"t__{v}": (r[v] if v == "state" else num(r[v])) for v in tvars}}
       for r in sorted(rows, key=lambda r: -r["uninsured"])])

# (6) DIVBAR -- illustrative Likert
likert = [
 ("Texas is on the right track investing in K-12 education",
   [("Strongly disagree",18),("Disagree",22),("Neutral",14),("Agree",29),("Strongly agree",17)]),
 ("Higher education is affordable for most Texas families",
   [("Strongly disagree",29),("Disagree",33),("Neutral",14),("Agree",18),("Strongly agree",6)]),
 ("Texas is prepared for its 20-year water-supply needs",
   [("Strongly disagree",21),("Disagree",28),("Neutral",22),("Agree",22),("Strongly agree",7)]),
]
dv = []
for q, lvls in likert:
    for lev, share in lvls:
        dv.append({"value": share, "name": q, "lev": lev})
build("06_divbar.html",
      dict(type="divbar", name="q", level="response", scheme="rdbu",
           levelorder="Strongly disagree|Disagree|Neutral|Agree|Strongly agree",
           centerlevel="Neutral", downloadpos="below", width=1040, height=440,
           title="Texans on state policy (illustrative survey data)",
           subtitle="Diverging stacked bar; neutral centered on zero",
           note="Illustrative survey data for demonstration only; not from County Health Rankings."),
      dv)

print("Built charts:", built)
