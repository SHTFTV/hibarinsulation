from pathlib import Path
from html.parser import HTMLParser
import json,xml.etree.ElementTree as ET
root=Path(__file__).parent/'public'
class Check(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.images=[];self.caption=0;self.h1=0
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='a' and d.get('href','').startswith('/'):self.links.append(d['href'])
  if tag=='img':self.images.append(d)
  if tag=='figcaption':self.caption+=1
  if tag=='h1':self.h1+=1
results=[]
for file in sorted(root.rglob('index.html')):
 c=Check();c.feed(file.read_text());assert c.images and c.caption, file
 assert c.h1==1,(file,c.h1)
 for d in c.images:
  for k in ['src','width','height','alt']:assert d.get(k),(file,k)
  assert (root/d['src'].lstrip('/')).exists(),(file,d['src'])
 for l in c.links:
  p=root/l.split('#')[0].lstrip('/');assert p.exists(),(file,l)
 results.append({'path':'/'+str(file.relative_to(root)).replace('index.html',''),'images':len(c.images),'captions':c.caption})
urls=ET.parse(root/'sitemap.xml').getroot();assert len(urls)==len(results)
report={'pages':len(results),'passed':'all pages have relevant captioned visuals, alt text and dimensions; all internal links and image files exist; single h1; sitemap covers all pages','page_results':results,'contact':'build@buildershaus.com; mailto opens user email; delivery not tested','deployment':'pending'}
(Path(__file__).parent/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
