"""Build the standalone technical opportunity underwriting document."""
from html import escape as esc
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DATA = ROOT / 'research/data/consumer-agent-uplift/map.json'


def build():
    data = json.loads(DATA.read_text())
    rubric = data['rubric']
    sources = {s['id']: s for s in data['sources']}
    sectors = {s['source_rank']: s for s in data['sectors']}
    assert sum(r['weight'] for r in rubric) == 100
    assert len(data['areas']) == 6 and len(sectors) == 15
    for area in data['areas']:
        assert set(area['scores']) == {r['id'] for r in rubric}
        assert all(isinstance(v, int) and 1 <= v <= 5 for v in area['scores'].values())
        assert all(x in sources for x in area['evidence'])
        assert len({e['sector'] for e in area['examples']}) >= 4
    total = lambda a: round(sum(a['scores'][r['id']] * r['weight'] / 5 for r in rubric))
    ordered = sorted(data['areas'], key=lambda a: (-total(a), a['name']))
    bullets = lambda items: '<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in items) + '</ul>'
    def sources_for(area):
        return ' · '.join(f'<a href="#source-{sid}">{sid}: {esc(sources[sid]["title"])}</a>' for sid in area['evidence'])
    rubric_html = ''
    for r in rubric:
        rubric_html += f'''<article class="rubric-card"><div class="kicker">{r['weight']}% of total</div><h3>{esc(r['name'])}</h3><p>{esc(r['question'])}</p><details><summary>Scoring anchors · 1 to 5</summary><ol>{''.join(f'<li>{esc(x)}</li>' for x in r['anchors'])}</ol></details><p class="small">{esc(r['notes'])}</p></article>'''
    rows = ''
    briefs = ''
    for index, a in enumerate(ordered, 1):
        rows += f'''<tr data-area="{a['id']}" data-total="{total(a)}" data-return="{a['scores']['return']}" data-speed="{a['scores']['speed']}" data-feasibility="{a['scores']['feasibility']}"><td class="number rank">{index}</td><th scope="row"><a href="#area-{a['id']}">{esc(a['name'])}</a><span class="sub">{esc(a['function'])}</span></th>{''.join(f'<td class="number">{a["scores"][r["id"]]}<span class="denominator"> / 5</span></td>' for r in rubric)}<td class="number total">{total(a)}<span class="denominator"> / 100</span></td><td>{esc(a['delivery']['first_build'])}<span class="sub">Engineering estimate</span></td></tr>'''
        score_reasons = ''.join(f'<div><dt>{esc(r["name"])} · {a["scores"][r["id"]]}/5</dt><dd>{esc(a["rationale"][r["id"]])}<small>Confidence: {a["confidence"][r["id"]]}</small></dd></div>' for r in rubric)
        examples = ''.join(f'<li><strong>{esc(sectors[e["sector"]]["short"])}</strong> — {esc(e["application"])}</li>' for e in a['examples'])
        briefs += f'''<details class="area-brief" id="area-{a['id']}" {'open' if index==1 else ''}><summary><span class="brief-index">{index:02}</span><span><span class="brief-name">{esc(a['name'])}</span><span class="sub">{esc(a['thesis'])}</span></span><span class="brief-score">{total(a)}<small>/ 100</small></span></summary><div class="brief-content">
<p class="scope"><strong>Representative scope.</strong> {esc(a['scope'])}</p>
<div class="two-col"><div><h4>EBITA mechanism</h4><p>{esc(a['economics']['mechanism'])}</p><h4>What has to become real</h4><p>{esc(a['economics']['conversion'])}</p></div><div><h4>Build and time to value</h4><p><strong>{esc(a['delivery']['first_build'])}</strong> for the first bounded implementation under the common assumptions.</p><p><strong>Economic observation:</strong> {esc(a['delivery']['economic_observation'])}</p><p class="small">Build time and economic observation are separate. These ranges are planning judgments, not researched delivery benchmarks.</p></div></div>
<h4>Score rationale</h4><dl class="rationale">{score_reasons}</dl>
<div class="two-col"><div><h4>Technical building blocks</h4>{bullets(a['technology'])}<h4>Ordinary data dependencies</h4>{bullets(a['data'])}</div><div><h4>Variation inside the area</h4><p><strong>Simpler scope:</strong> {esc(a['scope_variation']['simpler'])}</p><p><strong>More demanding scope:</strong> {esc(a['scope_variation']['harder'])}</p><h4>Technical uncertainties</h4>{bullets(a['technical_risks'])}</div></div>
<div class="two-col"><div><h4>Reusable core</h4><p>{esc(a['reusable'])}</p><h4>What changes between businesses</h4><p>{esc(a['adaptation'])}</p></div><div><h4>Build versus configure</h4><p>{esc(a['existing_alternatives'])}</p><h4>Benefit boundaries</h4><p>{esc(a['overlap'])}</p></div></div>
<div class="two-col"><div><h4>Examples across sectors</h4><ul>{examples}</ul></div><div><h4>Questions that could change the assessment</h4>{bullets(a['open_questions'])}</div></div>
<p class="evidence-links"><strong>Capability evidence:</strong> {sources_for(a)}</p></div></details>'''
    sector_rows = ''
    for s in data['sectors']:
        cells = ''.join(f'<td><span class="applicability {s["applicability"][a["id"]].lower()}">{s["applicability"][a["id"]]}</span></td>' for a in ordered)
        sector_rows += f'<tr data-exp="{int(s["lisa_experience"])}"><th scope="row"><a href="../reports/pe-opportunity-map.html#{s["id"]}">{esc(s["short"])}</a><span class="sub">Lisa experience: {"Yes" if s["lisa_experience"] else "Not marked"}</span></th>{cells}<td class="boundary">{esc(s["boundary"])}</td></tr>'
    sources_html = ''.join(f'<li id="source-{s["id"]}"><a href="{esc(s["url"], quote=True)}">{s["id"]} · {esc(s["title"])}</a>'+(f' · <a href="{esc(s["related_url"], quote=True)}">Event creation reference</a>' if s.get('related_url') else '')+f'<p>{esc(s["finding"])}</p></li>' for s in data['sources'])
    replacements = {'__RUBRIC__':rubric_html,'__RANKING__':rows,'__BRIEFS__':briefs,'__SECTOR_HEADERS__':''.join(f'<th scope="col">{esc(a["name"])}</th>' for a in ordered),'__SECTORS__':sector_rows,'__SOURCES__':sources_html,'__DATA__':json.dumps(data,ensure_ascii=False).replace('<','\\u003c')}
    html = (HERE/'template.html').read_text()
    for token,value in replacements.items():
        assert token in html, token
        html=html.replace(token,value)
    target=ROOT/'research/analyses/consumer-agent-uplift.html'
    target.write_text(html)
    print(f'Built {target.relative_to(ROOT)}: {len(ordered)} technical areas / {len(sectors)} illustrative sectors')

if __name__ == '__main__':
    build()
