import json
p='../../index.html'
s=open(p).read()
D=json.load(open('./dict.json'))
rt=open('./runtime.js').read()
rt=rt.replace('__I18N__',json.dumps(D,ensure_ascii=False,separators=(',',':')))
i=s.index('/*I18N_START*/');j=s.index('/*I18N_END*/')
s=s[:i]+'/*I18N_START*/'+rt+s[j:]
open(p,'w').write(s);print('injected',len(s))
