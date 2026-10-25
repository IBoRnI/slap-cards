import numpy as np
from PIL import Image
from scipy import ndimage as nd
D=Image.open('desk.jpg').convert('RGB').crop((0,316,2048,1816)).resize((1600,1000),Image.LANCZOS)
D.save('../build/u/desk.webp',quality=82,method=6)
Hd=np.asarray(Image.open('hand.png')).astype(float)
r,g,b,A=[Hd[...,i] for i in range(4)]
cuff=(b>r+10)
cuff=nd.binary_opening(cuff,iterations=2);cuff=nd.gaussian_filter(cuff.astype(float),1.2)
lum=.3*r+.59*g+.11*b
sk=(1-cuff)*(A>0);bs=np.median(lum[(cuff<.5)&(A>200)]);bc=np.median(lum[(cuff>.5)&(A>200)])
G={'glove_bare':None,'glove_school':('#5b8cff','#ffffff'),'glove_box':('#ff4d5e','#ffffff'),'glove_neon':('#3cf0ff','#ff5fa2'),'glove_dragon':('#2ad17c','#E9B21C'),'glove_gold':('#ffd84a','#ffffff')}
def hx(c):return np.array([int(c[i:i+2],16) for i in (1,3,5)],float)
def tint(c,k):
    k=k[...,None];return np.where(k<=1,c*k,c+(255-c)*np.clip(k-1,0,1)*1.2)
def out(a,n):
    im=Image.fromarray(a.clip(0,255).astype(np.uint8),'RGBA');im.thumbnail((240,400),Image.LANCZOS);im.save('../build/u/'+n+'.webp',quality=88,method=6);return im
ims=[]
for n,v in G.items():
    a=Hd.copy()
    if v:
        f,cf=hx(v[0]),hx(v[1])
        ks=np.clip(lum/bs,0,1.8);kc=np.clip(lum/bc,0,1.8)
        if v[1]=='#ffffff':cf=np.array([235,238,245.]);kc=np.clip(lum/bc*.92,0,1.3)
        col=tint(f,ks)*(1-cuff[...,None])+tint(cf,kc)*cuff[...,None]
        a[...,:3]=col
    ims.append(out(a,'h_'+n))
print(ims[0].size)
sh=Image.new('RGBA',(sum(i.width+10 for i in ims),ims[0].height),(28,32,71,255))
x=0
for i in ims:sh.alpha_composite(i,(x,0));x+=i.width+10
sh.convert('RGB').save('hchk.png')
