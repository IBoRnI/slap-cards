import random, statistics, json, sys
# ---- game data
TEAMS_R=[0,0,1,1,2,2,3,3,4]
TEAM_SIZE=[4,6,4,6,4,5,4,4,3]
CH=[]  # (id, rarity)
for t,(r,n) in enumerate(zip(TEAMS_R,TEAM_SIZE)):
    for i in range(n): CH.append((len(CH),r,t))
POOL={r:[c for c in CH if c[1]==r] for r in range(5)}
P=dict(
 gum_odds=[60,26,10,3.5,.5], mut=[4,1,.2], pity=80,
 break_odds=[40,32,20,7,1],
 rate=[.3,.7,1.6,3.6,8.0], mutmul=[1,1.6,2.6,4], lvlmul=.25,
 base_h=30, cap_h=8,
 slots_house=[5,6,7,8,9], house_p=[0,2000,15000,60000,250000],
 slot_p=[4000,12000,30000,70000,150000],
 decor_total=[500,1200,1500,3000,4000,6000,6000,8000,9000,12000,12000,12000,15000,18000,20000,20000,30000,50000],
 win_c=40, card_c=8, quest=360, rec_coin=2,
 lv_cost=[0,0,1,2,4,8],
)
class Player:
    def __init__(s,prof):
        s.prof=prof;s.album=set();s.dup={};s.coins=300;s.lvl={};s.pity=0;s.house=0;s.extra=0;s.decor=0;s.log={}
        for k in [(0,0),(1,0),(2,0),(4,0),(5,0),(9,0)]: s.album.add(k); s.dup[k]=2
    def gain(s,k):
        if k in s.album: s.dup[k]=s.dup.get(k,0)+1
        else: s.album.add(k)
    def roll(s,odds,mut,pity=False):
        r=random.choices(range(5),odds)[0]
        if pity:
            s.pity+=1
            if s.pity>=P['pity'] and r<4: r=4
            if r==4: s.pity=0
        c=random.choice(POOL[r]); x=random.random()*100
        m=3 if x<mut[2] else 2 if x<mut[2]+mut[1] else 1 if x<sum(mut) else 0
        return (c[0],m)
    def gum(s,odds=None,first=False):
        # pick 1 of 3: player picks best (highest rarity / new)
        ks=[s.roll(odds or P['gum_odds'],P['mut']) for _ in range(3)]
        s.pity+=1
        if s.pity>=P['pity'] and not any(CH[k[0]][1]==4 for k in ks): ks[0]=(random.choice(POOL[4])[0],0)
        if first: ks=[(random.choice(POOL[2])[0],0)]
        def score(k): return (k not in s.album)*10+CH[k[0]][1]*3+k[1]*2
        ch=random.choice(ks)
        if CH[ch[0]][1]==4: s.pity=0
        s.gain(ch)
    def slots(s): return P['slots_house'][s.house]+s.extra
    def val(s,k): return P['rate'][CH[k[0]][1]]*P['mutmul'][k[1]]*(1+P['lvlmul']*(s.lvl.get(k,1)-1))
    def rate_min(s):
        best=sorted(s.album,key=s.val,reverse=True)[:s.slots()]
        return sum(s.val(k) for k in best)
    def upgrade(s):
        # level up cards in yard with spare dups (keep 3 dups for matches)
        for k in sorted(s.album,key=s.val,reverse=True)[:s.slots()]:
            while s.lvl.get(k,1)<5:
                c=P['lv_cost'][s.lvl.get(k,1)+1]
                if s.dup.get(k,0)>=c: s.dup[k]-=c; s.lvl[k]=s.lvl.get(k,1)+1
                else: break
        # exchange 5->1 for commons/uncommons with extra
        for k,n in list(s.dup.items()):
            r=CH[k[0]][1]
            if r<4 and n>=8 and s.lvl.get(k,1)>=3 or (r<4 and n>=10):
                s.dup[k]-=5; s.gain((random.choice(POOL[r+1])[0],k[1]))
    def buy(s):
        # priority: next house when affordable, then slot, decor; keep reserve for gums? casual buys gum if coins>> 
        for _ in range(10):
            if s.house<4 and s.coins>=P['house_p'][s.house+1]: s.coins-=P['house_p'][s.house+1]; s.house+=1; continue
            if s.extra<5 and s.coins>=P['slot_p'][s.extra]*1.0 and (s.house>=1): s.coins-=P['slot_p'][s.extra]; s.extra+=1; continue
            if s.decor<len(P['decor_total']) and s.coins>=P['decor_total'][s.decor]*2: s.coins-=P['decor_total'][s.decor]; s.decor+=1; continue
            break
    def complete(s,r,m=0): return all((c[0],m) in s.album for c in POOL[r])
def sim(prof,days=90,seed=0):
    random.seed(seed);p=Player(prof);first=True
    ms={}
    for d in range(1,days+1):
        sess=prof['sessions']
        # free gums: first session 3, others min(3, gap/15)
        gap=16*60/(sess) if sess>1 else 600
        free=3+(sess-1)*min(3,int(gap/15))
        if d==1: free=min(free,1+(sess-1)*2)
        for i in range(free): p.gum(first=first); first=False
        for i in range(prof['ads']): p.gum()
        # breaks
        for i in range(prof['breaks']):
            if random.random()<prof['skill']: p.gain(p.roll(P['break_odds'],[10,3,.8]))
        # matches
        for i in range(prof['matches']):
            win=random.random()<(0.75 if d==1 else prof['winrate'])
            stake=sorted([CH[k[0]][1] for k,v in p.dup.items() for _ in range(v)])[:8]
            hand_r=stake[len(stake)//2] if stake else 0
            if win:
                n=random.randint(2,5)
                for _ in range(n):
                    r=max(0,min(4,hand_r+random.choice([-1,0,0,0,1])))
                    p.gain((random.choice(POOL[r])[0],1 if random.random()<.05 else 0))
                p.coins+=(P['win_c']+P['card_c']*n)*(1.5 if prof['nohint'] else 1)
            else:
                lose=random.randint(1,3)
                for _ in range(lose):
                    ks=[k for k,v in p.dup.items() if v>0]
                    if ks: k=min(ks,key=lambda k:CH[k[0]][1]); p.dup[k]-=1
        # record
        for i in range(prof['records']):
            sc=int(random.expovariate(1/prof['recavg']))
            p.coins+=sc*P['rec_coin']
        best=int(prof['recavg']*2.2)
        for j,m in enumerate([10,20,30]):
            if best>=m: p.gain((random.choice(POOL[j+1])[0],0))
        # quests, login
        p.coins+=P['quest']; p.gum()
        p.coins+=[100,150,0,250,300,0,600][(d-1)%7]
        if (d-1)%7 in (2,): p.gum()
        if (d-1)%7 in (5,6): p.gum([18,38,30,12,2])
        # bank income
        hours=min(P['cap_h'],8)+ (16 if sess>=3 else 8)
        p.coins+= (P['base_h']+p.rate_min()*60)*hours
        p.upgrade(); p.buy()
        # milestones
        chk={'house1':p.house>=1,'house2':p.house>=2,'house3':p.house>=3,'house4':p.house>=4,
             'common':p.complete(0),'uncommon':p.complete(1),'rare':p.complete(2),'epic':p.complete(3),'legend':p.complete(4),
             'first_leg':any(CH[k[0]][1]==4 for k in p.album),'gold_team':any(all((c[0],1) in p.album for c in CH if c[2]==t) for t in range(9)),
             'slots_max':p.extra>=5,'decor_all':p.decor>=len(P['decor_total'])}
        for k,v in chk.items():
            if v and k not in ms: ms[k]=d
    ms['album%']=round(len(p.album)/160*100);ms['rate/min']=round(p.rate_min(),1)
    return ms
PROF={
 'casual':dict(sessions=4,ads=5,breaks=2,matches=5,records=3,recavg=6,winrate=.5,skill=.55,nohint=False),
 'active':dict(sessions=7,ads=15,breaks=5,matches=12,records=6,recavg=9,winrate=.58,skill=.7,nohint=True),
}
if __name__=='__main__':
    if len(sys.argv)>1: P.update(json.loads(sys.argv[1]))
    for name,prof in PROF.items():
        runs=[sim(prof,120,s) for s in range(30)]
        keys=['house1','house2','house3','house4','common','uncommon','rare','first_leg','epic','legend','gold_team','slots_max','decor_all','album%','rate/min']
        out={}
        for k in keys:
            v=[r[k] for r in runs if k in r]
            out[k]=(round(statistics.median(v)) if v else '-', f"{len(v)}/30")
        print(name, json.dumps(out,ensure_ascii=False))
