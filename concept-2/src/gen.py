import json,math
d=json.load(open('data.json'));L=json.load(open('loader.json'))
def key(e): return '%d_%.4f_%.4f_%.4f'%(e[6],e[7],e[8],e[9])
PN=('P','Violet','Hovered','Signal','Candidate','Best fit')
persons=lambda a:[e for e in a if e[5] in PN]
dots=lambda a:[e for e in a if e[5] in ('D','Dot')]
cx,cy=720,449;SC=1.95
S00=persons(d['S00']);L1=persons(L['L1'])
def ctr(e,s=1):
    x=e[0]+e[2]/2;y=e[1]+e[3]/2;return (cx+(x-cx)*s,cy+(y-cy)*s)
pairs=sorted((math.dist(ctr(a),ctr(b,SC)),i,j) for i,a in enumerate(S00) for j,b in enumerate(L1))
ui=set();uj=set();m={}
for dd,i,j in pairs:
    if i in ui or j in uj: continue
    ui.add(i);uj.add(j);m[j]=i
faces={};people={}
def fid(e):
    k=key(e);faces.setdefault(k,[e[6],e[7],e[8],e[9]]);return k
# per-state crop tweak from Figma (e[14] = [tx,ty]) rides along as the 9th field
st=lambda e:[round(e[0],1),round(e[1],1),round(e[2],1),e[4],e[10],e[11],e[12] if e[12] else 0,e[13]]+([e[14]] if len(e)>14 and e[14] else [])
for j,b in enumerate(L1):
    if j in m:k=fid(S00[m[j]])
    else:
        k='L1x'+str(j);faces[k]=[b[6],b[7],b[8],b[9]]
    people.setdefault(k,{})['L1']=st(b)
for k in ['S00','S02','S03','S04','S05']:
    for e in persons(d[k]):people.setdefault(fid(e),{})[k]=st(e)
h={'faces':faces,'people':people,'L1d':[[round(e[0],1),round(e[1],1),round(e[2],1),e[6]] for e in dots(L['L1'])],
 'halo':[e for e in L['L0'] if e[5]=='H'][0][:4],
 'S04d':[[e[0],e[1],e[2],e[4]] for e in d['S04'] if e[5]=='Dot'],'S05d':[[e[0],e[1],e[2],e[4]] for e in d['S05'] if e[5]=='Dot'],
 'S04r':[[e[0],e[1],e[2]] for e in d['S04'] if e[5]=='Ring'],'S05r':[[e[0],e[1],e[2]] for e in d['S05'] if e[5]=='Ring'],
 'glow':[e[:4] for e in d['S05'] if e[5]=='Glow'],'pos':d['pos']}
# SHRINK: L0 dots are 60% of their old size, scaled around each dot's centre (matches Screen 1 in Figma)
L0=[[round(e[0]+e[2]*.2,1),round(e[1]+e[2]*.2,1),round(e[2]*.6,1),e[6]] for e in dots(L['L0'])]
els=[('d',i,e) for i,e in enumerate(h['L1d'])]+[('p',k,v['L1']) for k,v in people.items() if 'L1' in v]
c=lambda e:(e[0]+e[2]/2,e[1]+e[2]/2)
pairs=sorted((math.dist(c(a),c(b[2])),i,j) for i,a in enumerate(L0) for j,b in enumerate(els))
ui=set();uj=set();m2={}
for dd,i,j in pairs:
    if i in ui or j in uj: continue
    ui.add(i);uj.add(j);m2[j]=i
for j,(t,k,e) in enumerate(els):
    a=L0[m2[j]] if j in m2 else [e[0],e[1],e[2],0]
    if t=='d':h['L1d'][k]=h['L1d'][k]+a
    else:people[k]['L0']=a
# DANIEL: this person uses his own photo (sheet slot 4 = img/daniel.jpg, full frame)
if '1_0.5113_0.5079_0.1025' in faces: faces['1_0.5113_0.5079_0.1025']=[4,0,0,1]
json.dump(h,open('hero.json','w'),separators=(',',':'))
s0=set(k for k,v in people.items() if 'S00' in v);s2=set(k for k,v in people.items() if 'S02' in v)
print('people',len(people),'S00->S02 kept',len(s0&s2),'S00 only',len(s0-s2))
