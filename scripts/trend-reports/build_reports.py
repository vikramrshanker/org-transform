"""Rebuild the six September 2026 briefs from their maintained content modules.
The approved AI report supplies the shared, self-contained design only.
"""
from pathlib import Path
from html import escape
import json, re, runpy

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
pilot = (ROOT / 'trends/03-ai-capability-and-adoption.html').read_text()
STYLE = re.search(r'<style>(.*?)</style>', pilot, re.S).group(1)
SCRIPT = re.search(r'<script>(.*?)</script>', pilot, re.S).group(1)
STYLE += '''
/* Shared refinements for the six companion reports. */
.hero h1{max-width:1000px;font-size:clamp(44px,5.3vw,72px)}
.series-link{display:block;margin:24px 0 0;font-size:12px;color:var(--muted)}
.table-wrap table{min-width:640px}.numeric{text-align:right;white-space:nowrap}
.bar-row{grid-template-columns:220px minmax(0,1fr) 82px}.bar-row b{font-size:20px;text-align:right}
.bar-label{line-height:1.5}.source-list a{overflow-wrap:anywhere}
.case-grid{grid-template-columns:1fr 1fr}.case-metrics strong{font-size:34px}
.flow{counter-reset:flow}.flow>div{min-width:0}.flow p{font-size:13px}
.analysis-label{color:var(--green);font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
@media(max-width:650px){.hero h1{font-size:43px;line-height:1.05}.case-grid{grid-template-columns:1fr}.bar-row{grid-template-columns:minmax(0,1fr) 75px;gap:8px 14px}.bar-row .bar-label{grid-column:1/-1}.bar-row .bar-track{grid-column:1}.bar-row b{grid-column:2;font-size:20px}.case-metrics strong{font-size:30px}}
@media print{.hero h1{font-size:36pt}.table-wrap table{min-width:0}.bar-row{grid-template-columns:180px 1fr 65px}.case{break-inside:auto}.case h3,.case h4{break-after:avoid}.case-metrics{break-inside:avoid}.case-metrics strong{font-size:25pt}.source-list{columns:1}.series-link{display:none}}
'''

def cite(*ids):
    return '<sup>' + ', '.join(f'<a href="#s{i:02}">[{i}]</a>' for i in ids) + '</sup>'

def p(t, cls=''):
    return f'<p class="{cls}">{t}</p>'

def table(title, headers, rows):
    return f'<div class="table-wrap" role="region" tabindex="0" aria-label="{escape(title)}; scroll horizontally if needed"><table><caption>{title}</caption><thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(('<td class="numeric">' if j > 0 and re.fullmatch(r'[$−+\d][\d$.,%×+−/ →–mnb ]*', str(v)) else '<td>') + str(v) + '</td>' for j,v in enumerate(row)) + '</tr>' for row in rows) + '</tbody></table></div>'

def brief(items):
    return '<div class="brief-grid">'+''.join(f'<article><span class="number">{i:02}</span><h3>{h}</h3><p>{t}</p></article>' for i,(h,t) in enumerate(items,1))+'</div>'

def note(t): return '<div class="note">'+t+'</div>'

def flow(title, items, caption):
    return '<figure><div class="figure-head"><span>Workflow · analytical design</span><h3>'+title+'</h3></div><div class="flow">'+''.join(f'<div><b>{i:02} / {h}</b><p>{t}</p></div>' for i,(h,t) in enumerate(items,1))+'</div><figcaption>'+caption+'</figcaption></figure>'

def case(kicker, title, metrics, observed, interpretation, limit):
    return '<article class="case"><div class="case-meta">'+kicker+'</div><h3>'+title+'</h3><div class="case-metrics">'+''.join(f'<div><strong>{n}</strong><span>{label}</span></div>' for n,label in metrics)+'</div><div class="case-grid"><div><h4>What happened</h4>'+p(observed)+'</div><div><h4>What it suggests</h4>'+p(interpretation)+'</div></div><p class="case-bottom"><b>Evidence boundary.</b> '+limit+'</p></article>'

class Report:
    def __init__(self, slug, title, deck, scope):
        self.slug,self.title,self.deck,self.scope=slug,title,deck,scope
        self.sources=[]; self.sections=[]; self.evidence=[]
    def source(self,title,url,date,method,limit):
        self.sources.append(dict(id=len(self.sources)+1,title=title,url=url,published_or_version=date,method=method,limitations=limit,accessed='2026-09-21'))
    def section(self,id,label,title,body): self.sections.append((id,label,title,body))
    def chart(self,title,rows,max_value,unit,caption,source_ids,kind='observed',assumptions=None):
        self.evidence.append(dict(title=title,kind=kind,unit=unit,rows=[dict(label=l,value=v,display=d) for l,v,d in rows],scale_max=max_value,source_ids=source_ids,notes=re.sub('<[^>]*>','',caption),assumptions=assumptions))
        return '<figure><div class="figure-head"><span>'+('Illustrative calculation' if kind=='illustrative' else 'Evidence in view')+'</span><h3>'+title+'</h3></div><div class="bars">'+''.join(f'<div class="bar-row"><span class="bar-label">{l}</span><div class="bar-track" aria-hidden="true"><div class="bar" style="width:{v/max_value*100:.4f}%"></div></div><b>{d}</b></div>' for l,v,d in rows)+'</div><figcaption>'+caption+cite(*source_ids)+'</figcaption></figure>'
    def save(self):
        folder=ROOT/'research/data'/self.slug[3:];folder.mkdir(exist_ok=True)
        (folder/'sources.json').write_text(json.dumps(self.sources,indent=2,ensure_ascii=False)+'\n')
        (folder/'evidence.json').write_text(json.dumps(dict(research_date='2026-09-21',charts=self.evidence),indent=2,ensure_ascii=False)+'\n')
        (folder/'README.md').write_text(f'# {self.title}: evidence\n\nResearch checked September 21, 2026. Supports the [executive report](../../../trends/{self.slug}.html).\n\n- [Source register](sources.json): publication/version dates, methods, limitations and direct links. Numbering is local to this report.\n- [Chart values](evidence.json): transcribed values, units, denominators and illustration assumptions. Illustrations are calculations, not market estimates.\n- [Maintained report content](../../../scripts/trend-reports/{self.slug[:2]}.py): the full text, tables and case evidence.\n\nThis is a selected evidence review, not a systematic review. Sources were checked on the research date; observations retain their own dates. No interviews or proprietary datasets were obtained. Company disclosures do not establish causal effects. Older cases describe mechanisms, not current market prevalence. Sources are linked, not reproduced in full.\n\nWhen updating, preserve dated observations, verify the denominator and methodology, update the content and source records together, and regenerate using the shared builder. Recheck mobile and print layouts after changes.\n')
        links=''.join(f'<a href="#{id}"><span class="nav-index" aria-hidden="true">{i:02}</span><span>{label}</span></a>' for i,(id,label,_,_) in enumerate(self.sections))+'<a href="#sources"><span class="nav-index" aria-hidden="true">—</span><span>Sources</span></a>'
        nav=f'<nav aria-label="Report sections">{links}</nav>'
        body=''.join(f'<section id="{id}"><div class="eyebrow">{i:02} / {label}</div><h2>{title}</h2>{content}</section>' for i,(id,label,title,content) in enumerate(self.sections))
        appendix=f'<section class="sources" id="sources"><div class="eyebrow">Evidence appendix</div><h2>Sources, dates and limits</h2><p>{len(self.sources)} source entries. Research checked September 21, 2026. Observation periods appear alongside the claims. This is a selected review; it does not claim every series is current to the research date. Company accounts, surveys, forecasts and causal studies are identified separately. Opportunity assessments and financial illustrations are our analysis.</p><p><a href="../research/data/{self.slug[3:]}/sources.json">Structured source register</a> · <a href="../research/data/{self.slug[3:]}/evidence.json">Chart data and assumptions</a> · <a href="../research/data/{self.slug[3:]}/README.md">Update notes</a></p><ol class="source-list">'+''.join(f'<li id="s{s["id"]:02}"><a href="{escape(s["url"],quote=True)}">{escape(s["title"])} ↗</a><div class="source-date">{escape(s["published_or_version"])}</div><p><b>{escape(s["method"])}</b> {escape(s["limitations"])}</p></li>' for s in self.sources)+'</ol></section>'
        html=f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(self.title)} — Organizational Transformation</title><meta name="description" content="{escape(self.deck,quote=True)}"><style>{STYLE}</style></head><body><a class="skip-link" href="#report-content">Skip to report</a><header class="hero" id="top"><div class="eyebrow">Organizational Transformation / Market research / {self.slug[:2]}</div><h1>{escape(self.title)}</h1><div class="hero-bottom"><p class="deck">{self.deck}</p><div class="meta"><span>21 September 2026</span><span>Evidence review · Version 1</span><span>{self.scope}</span></div></div><a class="series-link" href="index.html">All market trends ↗</a></header><details class="mobile-contents"><summary>Contents <span class="nav-current">Executive brief</span></summary>{nav}<button class="print-button" onclick="window.print()">Print / save PDF ↗</button></details><div class="report-layout"><aside class="report-sidebar"><div class="nav-label">In this report</div>{nav}<button class="print-button" onclick="window.print()">Print / save PDF ↗</button></aside><main id="report-content">{body}{appendix}</main></div><footer>Organizational Transformation · Trend {self.slug[:2]} · Version 1 · 21 September 2026 <a href="#top">Back to top ↑</a></footer><script>{SCRIPT}</script></body></html>'
        (ROOT/'trends'/f'{self.slug}.html').write_text(html)
        print(f'{self.slug}: {len(self.sources)} sources; {len(self.evidence)} figures')

if __name__=='__main__':
    for number in ['01','02','04','05','06','07']:
        runpy.run_path(str(BASE/f'{number}.py'),init_globals=dict(Report=Report,cite=cite,p=p,table=table,brief=brief,note=note,flow=flow,case=case))
