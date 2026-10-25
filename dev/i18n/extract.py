import re, json, sys
src=open('../build/index.html').read()
CYR=re.compile('[Ѐ-ӿ]')
PH='\x00'
# --- JS tokenizer over <script> content
si=src.index('/*I18N_END*/')+12; se=src.rindex('</script>')
js=src[si:se]; html=src[:src.index('<script>')]
lits=[]  # (kind, text_with_PH, prev_code, next_code)
def parse_template(s,i):
    # s[i] is after backtick; returns (text_with_PH, nested_lits, end_index_after_backtick)
    out=[];i0=i
    while i<len(s):
        c=s[i]
        if c=='\\': out.append(s[i:i+2]); i+=2; continue
        if c=='`': return ''.join(out),i+1
        if c=='$' and s[i+1]=='{':
            j=parse_code(s,i+2,stop='}')
            out.append(PH); i=j; continue
        out.append(c); i+=1
    raise Exception('unterminated template')
def parse_quote(s,i,q):
    out=[]
    while s[i]!=q:
        if s[i]=='\\': out.append(s[i+1] if s[i+1] in "'\"\\" else s[i:i+2]); i+=2; continue
        out.append(s[i]); i+=1
    return ''.join(out),i+1
def parse_code(s,i,stop=None):
    depth=0
    while i<len(s):
        c=s[i]
        if c in "'\"":
            st=i; t,i=parse_quote(s,i+1,c); pre=s[max(0,st-3):st]; nxt=s[i:i+3]
            lits.append(('q',t,pre,nxt)); continue
        if c=='`':
            t,i=parse_template(s,i+1); lits.append(('t',t,'','')); continue
        if c=='/' and s[i+1]=='/':
            # comment unless inside regex-ish context: assume comment
            j=s.find('\n',i); i=j if j>0 else len(s); continue
        if c=='/' and s[i+1]=='*':
            i=s.find('*/',i)+2; continue
        if c=='/' :
            # regex literal detection: previous non-space char
            k=i-1
            while k>=0 and s[k] in ' \t': k-=1
            if k>=0 and s[k] in '(,=:[!&|?;{}+':
                j=i+1;cls=False
                while j<len(s):
                    if s[j]=='\\': j+=2; continue
                    if s[j]=='[': cls=True
                    elif s[j]==']': cls=False
                    elif s[j]=='/' and not cls: break
                    j+=1
                i=j+1
                while i<len(s) and s[i].isalpha(): i+=1
                continue
        if stop:
            if c=='{': depth+=1
            elif c=='}':
                if depth==0: return i+1
                depth-=1
        i+=1
    return i
parse_code(js,0)
keys={}
def addkey(t,src_kind):
    t=t.replace('\n',' ')
    t=re.sub(r'\s+',' ',t).strip()
    if not CYR.search(t): return
    keys[t.replace(PH,'{}')]=src_kind
TAG=re.compile(r'<[^>]*>')
ATTR=re.compile(r'(?:alt|title|aria-label|placeholder)="([^"]*)"')
for kind,t,pre,nxt in lits:
    if not CYR.search(t): continue
    for a in ATTR.findall(t): addkey(a,'attr')
    parts=TAG.split(t)
    if kind=='q' and len(parts)==1:
        tt=t
        if nxt.lstrip().startswith('+') : tt=tt+PH
        if pre.rstrip().endswith('+'): tt=PH+tt
        addkey(tt,'q')
        if tt!=t: addkey(t,'q')
    else:
        for p in parts: addkey(p,kind)
# static html
body=html[html.index('<body>'):] if '<body>' in html else html
for p in TAG.split(html[html.find('<div id="wrap"'):]): addkey(p,'html')
for a in ATTR.findall(html): addkey(a,'attr')
# also the tail html after script
for p in TAG.split(src[se:]): addkey(p,'html')
json.dump(sorted(keys),open('keys.json','w'),ensure_ascii=False,indent=0)
print(len(keys), sum(len(k) for k in keys))
