import os,numpy as np
from PIL import Image
from scipy import ndimage as nd
R='raw2/';O='../build/u/'
def bgmodel(im):
    h,w,_=im.shape;s=4
    sm=im[::s,::s];hh,ww=sm.shape[:2]
    yy,xx=np.mgrid[0:hh,0:ww];yy=yy/hh;xx=xx/ww
    b=int(min(hh,ww)*.05)
    m=np.zeros((hh,ww),bool);m[:b]=m[-b:]=True;m[:,:b]=m[:,-b:]=True
    A=np.stack([np.ones_like(xx),xx,yy,xx*xx,yy*yy,xx*yy],-1)
    Y,X=np.mgrid[0:h,0:w];Y=Y/h;X=X/w
    AF=np.stack([np.ones_like(X),X,Y,X*X,Y*Y,X*Y],-1)
    out=np.zeros_like(im)
    for c in range(3):
        co,*_=np.linalg.lstsq(A[m],sm[...,c][m],rcond=None);out[...,c]=AF@co
    return out
def cut(n,t0=7,t1=34,keep_shadow=True):
    im=np.asarray(Image.open(R+n+'.jpg').convert('RGB')).astype(float)
    bg=bgmodel(im)
    d=np.sqrt(((im-bg)**2).sum(-1))
    # luminance difference: darker pixels (shadow) vs others
    core=d>t1
    core=nd.binary_opening(core,iterations=2)
    lab,k=nd.label(core);sz=nd.sum(core,lab,range(1,k+1))
    core=np.isin(lab,[i+1 for i,s in enumerate(sz) if s>sz.max()*0.01])
    core=nd.binary_fill_holes(core)
    a=np.clip((d-t0)/(t1-t0),0,1)
    near=nd.binary_dilation(core,iterations=60)
    a=np.where(core,1,np.where(near,a,0))
    if not keep_shadow:
        dark=(im.mean(-1)<bg.mean(-1))&~core
        a=np.where(dark,a*0.0,a)
    a3=np.maximum(a,1e-3)[...,None]
    col=np.clip((im-(1-a3)*bg)/a3,0,255)
    col=np.where(a[...,None]>0.98,im,col)
    out=np.dstack([col,a*255]).astype(np.uint8)
    ys,xs=np.where(a>0.04);out=out[ys.min():ys.max()+1,xs.min():xs.max()+1]
    return Image.fromarray(out,'RGBA'),core[ys.min():ys.max()+1,xs.min():xs.max()+1]
def save(im,out,maxs,q=88):
    im.thumbnail((maxs,maxs),Image.LANCZOS);im.save(O+out+'.webp',quality=q,method=6);print(out,im.size)
for n,o,s in [('close','close',128),('gum_school','pk_school',320),('gum_super','pk_super',320),('gum_series','pk_series',320),('gum_free','pk_free',320),('logo','logo',900),('pedestal','pedestal',300)]+[('ic_'+x,'i_'+x,128) for x in ['bell','piggy','gift','quests','trophy','gear','bolt','stack','star']]:
    im,_=cut(n);save(im,o,s)
# card backs: tight rect from core bbox, rounded mask
for i in range(5):
    im0=np.asarray(Image.open(R+'back%d.jpg'%i).convert('RGB')).astype(float)
    _,core=None,None
    bg=bgmodel(im0);d=np.sqrt(((im0-bg)**2).sum(-1));core=d>40
    core=nd.binary_opening(core,iterations=3);lab,k=nd.label(core);sz=nd.sum(core,lab,range(1,k+1));core=lab==(np.argmax(sz)+1)
    # robust bbox: rows/cols where >50% filled
    rows=np.where(core.mean(1)>core.mean(1).max()*.6)[0];cols=np.where(core.mean(0)>core.mean(0).max()*.6)[0]
    y0,y1,x0,x1=rows.min(),rows.max(),cols.min(),cols.max()
    c=Image.fromarray(im0[y0:y1+1,x0:x1+1].astype(np.uint8)).resize((355,520),Image.LANCZOS).convert('RGBA')
    m=Image.new('L',c.size,0);from PIL import ImageDraw;ImageDraw.Draw(m).rounded_rectangle((0,0,354,519),radius=22,fill=255)
    c.putalpha(m);c.save(O+'back%d.webp'%i,quality=88,method=6);print('back',i,(x0,y0,x1,y1))
