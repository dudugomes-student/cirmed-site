import sys, numpy as np
from PIL import Image
def recolor(src, dst, target_h=201/360, ranges=((0.0,0.06),(0.72,1.0)), sat=0.95):
    im=Image.open(src).convert('RGBA'); a=np.asarray(im).astype(np.float32)/255
    rgb=a[...,:3]; alpha=a[...,3:]
    hsv=np.asarray(Image.fromarray((rgb*255).astype('uint8')).convert('HSV')).astype(np.float32)/255
    h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    m=np.zeros_like(h,bool)
    for lo,hi in ranges: m|=(h>=lo)&(h<=hi)
    m&=s>0.18
    h2=np.where(m,target_h,h); s2=np.where(m,np.clip(s*sat,0,1),s)
    # azul da marca é mais escuro que rosa/vermelho: escurece um pouco o que mudou de cor
    v2=np.where(m,v*0.86,v)
    out=Image.merge('HSV',[Image.fromarray((x*255).astype('uint8')) for x in (h2,s2,v2)]).convert('RGB')
    o=np.dstack([np.asarray(out),(alpha*255).astype('uint8')])
    Image.fromarray(o,'RGBA').save(dst)
if __name__=='__main__':
    recolor(sys.argv[1],sys.argv[2])
