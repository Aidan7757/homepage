#!/usr/bin/env python3
"""Generate the site from content.yaml.  Run: python3 build.py

Reads content.yaml and writes index.html + the three full-list pages.
No templating engine on purpose — plain string building, one dependency (pyyaml).
"""
from html import escape
import yaml

RED, GREEN = "%23c00", "%23090"


def ball(color):
    return (f"<img class=\"ball\" alt=\"o\" src=\"data:image/svg+xml,"
            f"%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14'"
            f"%3E%3Ccircle cx='7' cy='7' r='6' fill='{color}'/%3E%3C/svg%3E\" />")


def esc(s):
    return escape(str(s), quote=False) if s is not None else ""


def experience(groups):
    out = []
    for g in groups:
        out.append(f"\t\t\t<h4>{esc(g['org'])}</h4>")
        for r in g["roles"]:
            out.append(f"\t\t\t<p class=\"role\"><strong>{esc(r['role'])}</strong> "
                       f"<span class=\"dates\">{esc(r['dates'])}</span></p>")
            out.append(f"\t\t\t<p class=\"role-desc\">{esc(r['desc'])}</p>")
    return "\n".join(out)


def paper_li(p):
    parts = [f"<strong>{esc(p['title'])}</strong>"]
    if p.get("authors"):
        parts.append(esc(p["authors"]))
    if p.get("venue"):
        parts.append(esc(p["venue"]))
    if p.get("link"):
        parts.append(f'<a href="{escape(p["link"], quote=True)}" target="_blank" rel="noopener">Read</a>')
    return "\t\t\t\t<li>" + "<br>".join(parts) + "</li>"


def talk_li(t):
    parts = [f"<strong>{esc(t['title'])}</strong>"]
    if t.get("venue"):
        parts.append(esc(t["venue"]))
    if t.get("date"):
        parts.append(esc(t["date"]))
    return "\t\t\t\t<li>" + "<br>".join(parts) + "</li>"


def honor_li(h, full):
    parts = [f"<strong>{esc(h['title'])}</strong>", esc(h["date"])]
    if full and h.get("desc"):
        parts.append(esc(h["desc"]))
    return "\t\t\t\t<li>" + "<br>".join(parts) + "</li>"


def ul(items, render, **kw):
    return "\n".join(render(i, **kw) for i in items)


def selected(items):
    return [i for i in items if i.get("selected")]


HEAD = """<!DOCTYPE html>
<html lang="en">

<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1.0">
\t<title>{title}</title>
\t<link rel="icon" type="image/png" href="assets/favicon.png?v=4">
\t<link rel="stylesheet" href="style.css">
</head>

<body>
"""


def build_index(d):
    p = d["profile"]
    sel_papers = selected(d["papers"])
    sel_talks = selected(d["presentations"])
    sel_honors = selected(d["honors"])
    scholar = (f' &middot;\n\t\t\t\t\t<a href="{escape(p["scholar"], quote=True)}" '
               f'target="_blank" rel="noopener">Google Scholar</a>') if p.get("scholar") else ""

    return HEAD.format(title=f"{esc(p['name'].title())}'s Homepage") + f"""\t<div id="page">
\t\t<div id="left">
\t\t\t<div id="main">
\t\t\t\t<h1>{esc(p['name'])}</h1>
\t\t\t\t<h2 id="position">{esc(p['title'])}</h2>

\t\t\t\t<div class="address">
\t\t\t\t\t<p id="university">{esc(p['university'])}</p>
\t\t\t\t\t<p>Email: <a id="email" href="mailto:{esc(p['email'])}">{esc(p['email'])}</a></p>
\t\t\t\t</div>

\t\t\t\t<div class="bio">
\t\t\t\t\t<p><b>Biography:</b> <span id="biography">{esc(p['bio'])}</span></p>
\t\t\t\t</div>

\t\t\t\t<div class="cv">
\t\t\t\t\t<p><b>Curriculum Vitae:</b> <a id="cv" href="{esc(p['cv'])}" target="_blank">Curriculum Vitae</a>{scholar}
\t\t\t\t\t</p>
\t\t\t\t</div>
\t\t\t</div>

\t\t\t<h3>{ball(RED)} Research Experience</h3>
\t\t\t<div id="research_experience">
{experience(d['research'])}
\t\t\t</div>

\t\t\t<h3>{ball(GREEN)} Professional Experience</h3>
\t\t\t<div id="professional_experience">
{experience(d['professional'])}
\t\t\t</div>
\t\t</div>

\t\t<div id="right">
\t\t\t<img id="photo" src="{esc(p['photo'])}" alt="{esc(p['name'].title())}" title="{esc(p['name'].title())}" />
\t\t\t<p class="caption"><i>{esc(p['photo_caption'])}</i></p>

\t\t\t<h3>{ball(RED)} Selected Papers</h3>
\t\t\t<ul id="papers">
{ul(sel_papers, paper_li)}
\t\t\t</ul>
\t\t\t<p class="more"><a href="papers.html">Complete list of papers &rarr;</a></p>

\t\t\t<h3>{ball(GREEN)} Selected Presentations</h3>
\t\t\t<ul id="presentations">
{ul(sel_talks, talk_li)}
\t\t\t</ul>
\t\t\t<p class="more"><a href="presentations.html">Complete list of presentations &rarr;</a></p>

\t\t\t<h3>{ball(RED)} Selected Honors &amp; Awards</h3>
\t\t\t<ul id="honors_awards">
{ul(sel_honors, honor_li, full=False)}
\t\t\t</ul>
\t\t\t<p class="more"><a href="honors.html">Complete list of honors &amp; awards &rarr;</a></p>
\t\t</div>
\t</div>

\t<p class="footer" id="last_updated">Last updated {esc(p['updated'])}</p>
</body>

</html>
"""


def build_list(title, heading, color, list_id, body):
    return HEAD.format(title=f"Aidan Chadha — {title}") + f"""\t<div id="listpage">
\t\t<p class="backlink"><a href="index.html">&larr; Back to homepage</a></p>
\t\t<h3>{ball(color)} {heading}</h3>
\t\t<ul id="{list_id}">
{body}
\t\t</ul>
\t</div>
</body>

</html>
"""


def main():
    with open("content.yaml", encoding="utf-8") as f:
        d = yaml.safe_load(f)

    pages = {
        "index.html": build_index(d),
        "papers.html": build_list("Papers", "Papers", RED, "papers",
                                   ul(d["papers"], paper_li)),
        "presentations.html": build_list("Presentations", "Presentations", GREEN, "presentations",
                                          ul(d["presentations"], talk_li)),
        "honors.html": build_list("Honors & Awards", "Honors &amp; Awards", RED, "honors_awards",
                                   ul(d["honors"], honor_li, full=True)),
    }
    for name, html in pages.items():
        assert "<li>" in html, f"{name} came out empty"  # ponytail: cheap sanity check
        with open(name, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
