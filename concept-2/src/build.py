import re,base64
s=open('index.html').read()
def uri(f):
    ext=f.rsplit('.',1)[1];m={'jpg':'image/jpeg','png':'image/png','webp':'image/webp','woff2':'font/woff2'}[ext]
    return 'data:%s;base64,%s'%(m,base64.b64encode(open(f,'rb').read()).decode())
s=re.sub(r'(src=")(img/[^"]+)"',lambda m:m.group(1)+uri(m.group(2))+'"',s)
s=re.sub(r'url\((fonts/[^)]+)\)',lambda m:'url('+uri(m.group(1))+')',s)
s=re.sub(r"'(img/(?:sheet\d|daniel)\.jpg)'",lambda m:"'"+uri(m.group(1))+"'",s)
s=s.replace('/*DATA*/null',open('hero.json').read())
assert 'img/' not in s.replace('data:image','') and 'fonts/' not in s
open('articuler-concept-2-hero.html','w').write(s);print(len(s)//1024,'KB')
