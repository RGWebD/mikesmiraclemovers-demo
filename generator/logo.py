"""Hand-built vector logo for Mike's Miracle Movers: winged moving box (their wings mark + truck slab lettering). Text -> paths."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'..','brand'); os.makedirs(OUT,exist_ok=True)
INK='#17140F'; KRAFT='#C8975A'; KRAFT_D='#9C6F3A'; PAPER='#F6EEDF'; RED='#D62F1F'; BLUE='#2347A8'
_f={}
def font(n):
    if n not in _f: _f[n]=TTFont(os.path.join(HERE,'fonts',n))
    return _f[n]
def text_path(s,fn,size,x,y,track=0):
    f=font(fn); gs=f.getGlyphSet(); cmap=f.getBestCmap(); sc=size/f['head'].unitsPerEm
    pen=SVGPathPen(gs); cx=x
    for ch in s:
        g=cmap.get(ord(ch))
        if g is None: continue
        gs[g].draw(TransformPen(pen,(sc,0,0,-sc,cx,y))); cx+=gs[g].width*sc+track
    return pen.getCommands(), cx-track-x
from fontTools.pens.boundsPen import BoundsPen
def tbounds(s,fn,size,track=0):
    f=font(fn); gs=f.getGlyphSet(); cmap=f.getBestCmap(); sc=size/f['head'].unitsPerEm
    pen=BoundsPen(gs); cx=0
    for ch in s:
        g=cmap.get(ord(ch)); gs[g].draw(TransformPen(pen,(sc,0,0,-sc,cx,0))); cx+=gs[g].width*sc+track
    return pen.bounds
def tw(s,fn,size,track=0): return text_path(s,fn,size,0,0,track)[1]
SLAB='AlfaSlabOne-Regular.ttf'; MARK='PermanentMarker-Regular.ttf'

def wing(side, col, simple=False):
    """swept feather bands leaving the box edge; side=-1 left, 1 right. box spans x -30..30, y -24..28"""
    bands=[(-22,12,66,-44),(-7,11.5,58,-28),(8,11,48,-12),(20,8,36,4)] if not simple else [(-22,18,30,-36),(2,17,24,-12)]
    d=''
    for (y0,t,L,ty) in bands:
        x0=(30-2)*side; tx=(30+L)*side
        d+=(f'M{x0} {y0}C{x0+side*L*.4:.1f} {y0-3:.1f} {x0+side*L*.78:.1f} {ty+8:.1f} {tx} {ty}'
            f'C{x0+side*L*.8:.1f} {ty+t+7:.1f} {x0+side*L*.42:.1f} {y0+t+2:.1f} {x0} {y0+t}Z')
    return f'<path fill="{col}" d="{d}"/>'

def emblem(body=KRAFT, lid=KRAFT_D, tape=RED, mm=INK, wingc=INK, simple=False):
    """centered at 0,0; box 60x52 (x -30..30, y -24..28); wings to about +-96"""
    g=wing(-1,wingc,simple)+wing(1,wingc,simple)
    g+=f'<rect x="-30" y="-24" width="60" height="52" rx="3.5" fill="{body}"/>'
    g+=f'<rect x="-30" y="-24" width="60" height="12" rx="3.5" fill="{lid}"/><rect x="-30" y="-15" width="60" height="3" fill="{lid}"/>'
    g+=f'<rect x="-6" y="-24" width="12" height="{25 if not simple else 12}" fill="{tape}"/>'
    txt='MM' if not simple else 'M'
    size=27 if not simple else 34
    xmin,ymin,xmax,ymax=tbounds(txt,SLAB,size,-0.6)
    top=-7 if not simple else -10; bot=24
    sc=min((bot-top)/(ymax-ymin), 52/(xmax-xmin))
    p,_=text_path(txt,SLAB,size,0,0,-0.6)
    cx=(xmin+xmax)/2; cy=(ymin+ymax)/2
    g+=f'<path fill="{mm}" transform="translate(0 {(top+bot)/2:.2f}) scale({sc:.3f}) translate({-cx:.2f} {-cy:.2f})" d="{p}"/>'
    return g

def svg(vb,inner,title="Mike's Miracle Movers, L.L.C."):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}"><title>{title}</title>{inner}</svg>\n'

def wordmark(x,y,ink,accent,size=1.0,tag=True,tagc=None):
    """stacked truck-style lettering: MIKE'S / MIRACLE MOVERS + marker tagline. returns svg, width, height"""
    s1,w1=text_path("MIKE\u2019S",SLAB,20*size,0,0,1.2*size)
    s2,w2=text_path("MIRACLE MOVERS",SLAB,30*size,0,0,0.4*size)
    out=f'<path fill="{accent}" transform="translate({x} {y+19*size:.1f})" d="{s1}"/>'
    out+=f'<path fill="{ink}" transform="translate({x} {y+49*size:.1f})" d="{s2}"/>'
    h=52*size
    if tag:
        s3,w3=text_path("We make it look EASY!",MARK,15*size,0,0,0.3*size)
        out+=f'<path fill="{tagc or accent}" transform="translate({x+1} {y+70*size:.1f})" d="{s3}"/>'; h=74*size
    return out,max(w1,w2),h

def build():
    files={}
    # horizontal: emblem left, wordmark right
    for mode,ink,acc in [('light',INK,RED),('dark',PAPER,RED)]:
        em=emblem(wingc=ink, mm=INK)
        wm,ww,wh=wordmark(196,10,ink,acc)
        W=196+ww+6
        files[f'logo-horizontal-{mode}.svg']=svg(f'0 0 {W:.0f} 92',f'<g transform="translate(98 46) scale(.92)">{em}</g>{wm}')
    # stacked
    for mode,ink,acc in [('light',INK,RED),('dark',PAPER,RED)]:
        em=emblem(wingc=ink, mm=INK)
        wm,ww,wh=wordmark(0,0,ink,acc,1.0)
        W=max(ww,200)+20
        files[f'logo-stacked-{mode}.svg']=svg(f'0 0 {W:.0f} {96+wh+10:.0f}',f'<g transform="translate({W/2:.1f} 48)">{em}</g><g transform="translate({(W-ww)/2:.1f} 92)">{wm}</g>')
    # emblem only + one-colour
    files['emblem.svg']=svg('-100 -54 200 88',emblem())
    files['emblem-dark.svg']=svg('-100 -54 200 88',emblem(wingc=PAPER))
    files['emblem-mono-ink.svg']=svg('-100 -54 200 88',emblem(body=INK,lid=INK,tape=INK,mm=PAPER,wingc=INK).replace(f'fill="{INK}" d="M','fill="'+INK+'" d="M'))
    one=lambda c,bg: emblem(body=c,lid=c,tape=bg,mm=bg,wingc=c)
    files['emblem-mono-white.svg']=svg('-100 -54 200 88',one('#ffffff',INK))
    wm,ww,wh=wordmark(196,10,INK,INK,tagc=INK); files['logo-horizontal-mono.svg']=svg(f'0 0 {196+ww+6:.0f} 84',f'<g transform="translate(98 46) scale(.92)">{one(INK,"#ffffff")}</g>{wm}')
    # favicon: red rounded tile, kraft box + 2 bold wings
    fav=f'<rect width="64" height="64" rx="14" fill="{INK}"/><g transform="translate(32 33) scale(.47)">{emblem(wingc=PAPER,simple=True)}</g>'
    files['favicon.svg']=svg('0 0 64 64',fav)
    for k,v in files.items(): open(os.path.join(OUT,k),'w').write(v)
    # presentation sheet
    sw=''.join(f'<g transform="translate({60+i*170} 520)"><rect width="150" height="90" rx="10" fill="{c}" stroke="#0002"/><text x="0" y="114" font-family="monospace" font-size="15" fill="{INK}">{n} {c}</text></g>' for i,(n,c) in enumerate([('Ink',INK),('Kraft',KRAFT),('Kraft dark',KRAFT_D),('Paper',PAPER),('Cab red',RED),('Blanket blue',BLUE)]))
    sheet=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 680"><rect width="1100" height="680" fill="{PAPER}"/>
<rect x="560" y="30" width="510" height="240" rx="16" fill="{INK}"/>
<g transform="translate(40 60) scale(1.2)">{files['logo-horizontal-light.svg'].split('</title>',1)[1].rsplit('</svg>',1)[0]}</g>
<g transform="translate(590 100) scale(.85)">{files['logo-horizontal-dark.svg'].split('</title>',1)[1].rsplit('</svg>',1)[0]}</g>
<g transform="translate(150 360)">{emblem()}</g><g transform="translate(400 360)">{one(INK,"#fff")}</g>
<rect x="560" y="300" width="160" height="120" rx="12" fill="{INK}"/><g transform="translate(640 362)">{one("#fff",INK)}</g>
<g transform="translate(780 310) scale(1.6)">{fav}</g><g transform="translate(900 330) scale(.75)">{fav}</g><g transform="translate(960 340) scale(.5)">{fav}</g><g transform="translate(1000 345) scale(.25)">{fav}</g>
<text x="60" y="490" font-family="sans-serif" font-size="16" fill="{INK}">Display: Alfa Slab One (from the truck's slab lettering) · Labels: Permanent Marker · Body: DM Sans</text>{sw}</svg>'''
    open(os.path.join(OUT,'logo-sheet.svg'),'w').write(sheet)
    print('logo files',len(files)+1)
if __name__=='__main__': build()
