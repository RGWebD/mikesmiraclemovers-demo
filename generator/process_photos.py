"""Curate + export Mike's Miracle Movers photos to WebP. Plates/other brands/building numbers blurred, UI marks cropped."""
from PIL import Image, ImageFilter, ImageOps
import imagehash, os, itertools
SRC='/workspace/site3-research/photos/'
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','img'); os.makedirs(OUT,exist_ok=True)
KEEP=['g01','g02','g03','g04','g05','g06','g07','g09','g11']
CLONE={'g01':[((14,0,108,78),(120,0))]}   # app/share icon overlay in the corner -> cloned from adjacent foliage
BLUR={'g01':[(1180,740,1280,870)],   # rental-company logo on the mud flap   # rental-company logo on the mud flap
      'g02':[(455,35,830,192),       # other businesses' signs on the building
             (705,300,775,345),      # building number
             (1150,405,1264,480),    # other company's sign / truck at right
             (895,520,965,565)]}     # parked car's plate
CROP={'g05':(0,20,1284,939)}         # black bar along the top
hs={}
for k in KEEP:
    im=ImageOps.exif_transpose(Image.open(SRC+k+'.jpg')).convert('RGB')
    for b,src in CLONE.get(k,[]):
        w,h=b[2]-b[0],b[3]-b[1]; patch=im.crop((src[0],src[1],src[0]+w,src[1]+h))
        m=Image.new('L',(w,h),0); m.paste(255,(8,0,w-8,h-8)); m=m.filter(ImageFilter.GaussianBlur(6))
        im.paste(patch,b[:2],m)
    for b in BLUR.get(k,[]):
        pad=10; bb=(max(0,b[0]-pad),max(0,b[1]-pad),min(im.width,b[2]+pad),min(im.height,b[3]+pad))
        reg=im.crop(bb)
        for _ in range(3): reg=reg.filter(ImageFilter.GaussianBlur(12))
        m=Image.new('L',reg.size,0); m.paste(255,(pad,pad,reg.width-pad,reg.height-pad)); m=m.filter(ImageFilter.GaussianBlur(5))
        im.paste(reg,bb[:2],m)
    if k in CROP: im=im.crop(CROP[k])
    hs[k]=imagehash.phash(im)
    big=im.copy(); big.thumbnail((1600,1600)); big.save(f'{OUT}/{k}.webp','WEBP',quality=82,method=6)
    sm=im.copy(); sm.thumbnail((720,720)); sm.save(f'{OUT}/{k}-s.webp','WEBP',quality=78,method=6)
    print(k, im.size)
for a,b in itertools.combinations(hs,2):
    if hs[a]-hs[b]<14: print('close',a,b,hs[a]-hs[b])
og=Image.open(SRC+'g01.jpg').convert('RGB'); w,h=og.size
og=og.crop((0,int(h*.06),w,int(h*.06)+int(w*630/1200))).resize((1200,630)); og.save(f'{OUT}/og-base.jpg',quality=85)
print('done')
