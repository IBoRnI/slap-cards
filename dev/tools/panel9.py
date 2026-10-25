import numpy as np,os
from PIL import Image
from scipy import ndimage as nd
P=np.asarray(Image.open('panel.png')).astype(float)
o=24
def comp(src,c0,ts,te,c1,axis):
    # src array, left corner [0:c0], tile [ts:te], right corner [c1:end] along axis
    S=np.moveaxis(src,axis,0)
    L=S[:c0].copy();T=S[ts:te].copy();R=S[c1:].copy()
    a=(np.arange(o)/o)[:,None,None]
    T[:o]=(1-a)*S[te:te+o]+a*S[ts:ts+o]          # tile seamless start
    L[c0-o:]=(1-a)*S[c0-o:c0]+a*S[ts-o:ts]        # corner end -> tile start
    L[c0-o:]=(1-a)*S[c0-o:c0]+a*S[te-o:te]        # tile start ~ src[te]
    R[:o]=(1-a)*S[te:te+o]+a*S[c1:c1+o]           # tile end -> right corner
    out=np.concatenate([L,T,R],0)
    return np.moveaxis(out,0,axis),(c0,te-ts,S.shape[0]-c1)
H1,sx=comp(P,301,620,940,1270,1)
H2,sy=comp(H1,275,536,831,1075,0)
print('slices x',sx,'y',sy,H2.shape)
# make navy interior transparent
r,g,b,A=[H2[...,i] for i in range(4)]
lum=.3*r+.59*g+.11*b
navy=(b>r+6)&(lum<120)
lab,n=nd.label(navy);c=lab[H2.shape[0]//2,H2.shape[1]//2];m=lab==c
m=nd.binary_fill_holes(m)
# keep ornaments: gold pixels inside stay
gold=(r>150)&(r-b>60)
m&=~nd.binary_dilation(gold,iterations=2)
dist=nd.distance_transform_edt(m)
H2[...,3]=np.where(m,np.clip(1-dist/6,0,1)*A*0.0+A*np.clip(1-dist/3,0,1),A)
os.makedirs('../build/u',exist_ok=True)
im=Image.fromarray(H2.clip(0,255).astype(np.uint8),'RGBA');im.save('../build/u/panel.webp',quality=88,method=6)
bg=Image.new('RGBA',im.size,(40,46,110,255));bg.alpha_composite(im);bg.convert('RGB').resize((im.width*3//4,im.height*3//4)).save('pchk.png')
print(sx,sy)
