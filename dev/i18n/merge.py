import json,glob,re
L=['en','es','pt','de','fr','pl','cs','tr','id','hi']
D={l:{} for l in L}
bad=0
for f in sorted(glob.glob('tr_*.tsv')):
    for n,line in enumerate(open(f).read().split('\n')):
        if not line.strip(): continue
        c=line.split('\t')
        if len(c)!=11: print('COLS',f,n,len(c),line[:60]); bad+=1; continue
        k=c[0]; ph=k.count('{}')
        for l,v in zip(L,c[1:]):
            vp=len(re.findall(r'\{\d?\}',v))
            if vp!=ph: print('PH',f,n,l,k[:40],'|',v[:50]); bad+=1
            D[l][k]=v
keys=json.load(open('keys.json'))
miss=[k for k in keys if k not in D['en']]
print('rows',len(D['en']),'bad',bad,'missing',len(miss))
for m in miss: print('  MISS',m)
json.dump(D,open('dict.json','w'),ensure_ascii=False)
