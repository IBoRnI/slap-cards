import numpy as np,colorsys,os
from PIL import Image
from scipy import ndimage as nd
O='../build/u/';os.makedirs(O,exist_ok=True)
def save(a,n,maxw=None,maxh=None,q=86):
    im=Image.fromarray(a.astype(np.uint8),'RGBA') if isinstance(a,np.ndarray) else a
    if maxw or maxh:
        im.thumbnail((maxw or 99999,maxh or 99999),Image.LANCZOS)
    im.save(O+n+'.webp',quality=q,method=6);print(n,im.size,os.path.getsize(O+n+'.webp')//1024,'KB')
# panel 9-slice composite
P=np.asarray(Image.open('panel.png'))
H,W=P.shape[:2]
xs=[(0,301),(620,940),(1290,W)];ys=[(0,260),(536,831),(1095,H)]
rows=[np.concatenate([P[a:b,c:d] for c,d in xs],1) for a,b in ys]
pc=np.concatenate(rows,0);print('panel slices',[b-a for a,b in ys],[d-c for c,d in xs],pc.shape)
save(pc,'panel')
# button variants
B=np.asarray(Image.open('btn.png')).astype(float)
rgb=B[...,:3]/255;hsv=np.vectorize(colorsys.rgb_to_hsv)
r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
mx=rgb.max(-1);mn=rgb.min(-1);s=(mx-mn)/np.maximum(mx,1e-6);v=mx
hue=np.zeros_like(mx);d=np.maximum(mx-mn,1e-6)
hue=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60
yel=(hue>28)&(hue<60)&(v>0.62)&(s>0.25)
lab,n=nd.label(yel);cy,cx=B.shape[0]//2,B.shape[1]//2
m=lab==lab[cy,cx];m=nd.binary_fill_holes(m)
m=nd.binary_dilation(m,iterations=2)
soft=nd.gaussian_filter(m.astype(float),1.5)
print('yellow mask px',m.sum())
lum=(0.3*r+0.59*g+0.11*b)
base=np.median(lum[m])
def variant(col,name,gain=1.0):
    c=np.array([int(col[i:i+2],16) for i in (1,3,5)])/255
    k=np.clip(lum/base,0,2)**gain
    # shade: below 1 multiply, above 1 blend to white
    out=np.where(k[...,None]<=1,c*k[...,None],c+(1-c)*np.clip(k[...,None]-1,0,1)*1.6)
    out=np.clip(out,0,1)
    res=B.copy();res[...,:3]=rgb*255*(1-soft[...,None])+out*255*soft[...,None]
    return res
save(B,'btn_y',maxw=900)
save(variant('#f0458c','pink'),'btn_p',maxw=900)
save(variant('#2ea6ea','blue'),'btn_b',maxw=900)
save(variant('#27c46b','green'),'btn_g',maxw=900)
save(variant('#3d4488','ghost',1.15),'btn_d',maxw=900)
print('btn size',B.shape)
for n,s_ in [('coin',96),('album',220),('gum',220),('gum2',220),('shop',220)]:
    save(Image.open(n+'.png'),n,maxw=s_,maxh=s_,q=90)
# desk
D=Image.open('desk.jpg').convert('RGB');print(D.size)
