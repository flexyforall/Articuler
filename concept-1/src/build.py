import re,base64,json,collections
s=open('index.html').read()
def uri(f):
    m='image/png' if f.endswith('png') else 'image/jpeg'
    return 'data:%s;base64,%s'%(m,base64.b64encode(open('img/'+f,'rb').read()).decode())
cnt=collections.Counter(re.findall(r'src="img/([^"]+)"',s))
shared={f for f,c in cnt.items() if c>1}
S={}
def rep(m):
    f=m.group(1)
    if f in shared:
        S[f]=uri(f); return 'data-shared="%s"'%f
    return 'src="%s"'%uri(f)
s=re.sub(r'src="img/([^"]+)"',rep,s)
th=json.dumps([uri('T%d.jpg'%i) for i in range(1,14)])
s=s.replace("var THUMB=DATA.map(function(_,i){return 'img/T'+(i+1)+'.jpg';});","var THUMB=%s;"%th)
h=json.dumps({'H%d'%i:uri('H%d.png'%i) for i in range(1,14)})
s=s.replace("im.src='img/'+d[0]+'.png';","im.src=HIMG[d[0]];")
s=s.replace("var THUMB=","var HIMG=%s;\n  var THUMB="%h,1)
pre='<script>var SHARED=%s;</script>'%json.dumps(S)
fill='<script>[].forEach.call(document.querySelectorAll("img[data-shared]"),function(i){i.src=SHARED[i.getAttribute("data-shared")];});</script>'
i=s.find('<div id="site">'); s=s[:i]+pre+s[i:]
j=s.find('<script>',s.find('<div class="hint"')); s=s[:j]+fill+s[j:]
assert 'img/' not in s.replace('data:image','')
if '<meta charset' not in s: s='<meta charset="utf-8">\n'+s
open('articuler-motion-prototype.html','w').write(s); print(len(s)//1024,'KB', sorted(shared))
