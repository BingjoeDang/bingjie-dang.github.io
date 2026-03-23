from scholarly import scholarly
from scholarly import ProxyGenerator
import json

pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)

author = scholarly.search_author_id("Mfp83rUAAAAJ")
author = scholarly.fill(author, sections=['publications'])

data = []

for pub in author['publications']:
    pub = scholarly.fill(pub)
    title = pub['bib']['title']
    citations = pub.get('num_citations', 0)

    data.append({
        "title": title,
        "citations": citations
    })

with open("citations.json", "w") as f:
    json.dump(data, f, indent=2)
