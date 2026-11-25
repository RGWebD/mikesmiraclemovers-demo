import asyncio, json, sys, os
from playwright.async_api import async_playwright
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8822/'
TAG=sys.argv[2] if len(sys.argv)>2 else 'r1'
OUT='/workspace/mmm-work/qa-'+TAG; os.makedirs(OUT,exist_ok=True)
PAGES=['index.html','services.html','work.html','about.html','reviews.html','contact.html']
async def run():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for w,h in [(1440,900),(390,844)]:
      for pg_ in PAGES:
        ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=1 if w>500 else 2,is_mobile=w<500,has_touch=w<500)
        pg=await ctx.new_page(); errs=[]
        pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto(BASE+pg_,wait_until='load'); await pg.wait_for_timeout(2600)
        n=pg_.replace('.html','')
        await pg.screenshot(path=f'{OUT}/{n}-{w}-hero.png')
        H=await pg.evaluate('document.body.scrollHeight')
        y=0
        while y<H:
          y+=500; await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(110)
          H=await pg.evaluate('document.body.scrollHeight')
        await pg.wait_for_timeout(2300)
        r=await pg.evaluate('''()=>{
          const ov=document.documentElement.scrollWidth>window.innerWidth+1;
          const wide=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+2&&getComputedStyle(e).position!=='fixed'&&!e.closest('.marq,.tape-marq,.sc-grid,.jump-in,.hero,.phero,.cta,.mmenu,.loader,.tape-strip,.cta-tape')&&r.width>0}).slice(0,5).map(e=>(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)||e.tagName);
          const broken=[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.getAttribute('src')).map(i=>i.src);
          const srcs=[...document.querySelectorAll('main img[src]')].map(i=>i.getAttribute('src').replace('-s.webp','.webp')).filter(s=>s.startsWith('img/'));
          const dup=srcs.filter((s,i)=>srcs.indexOf(s)!==i);
          let ld=[];document.querySelectorAll('script[type="application/ld+json"]').forEach(s=>{try{ld.push(JSON.parse(s.textContent)['@type'])}catch(e){ld.push('INVALID')}});
          const cnt=[...document.querySelectorAll('[data-to]')].map(e=>e.textContent+'/'+e.dataset.to);
          const hidden=[...document.querySelectorAll('.rv,.split')].filter(e=>!e.classList.contains('in')).length;
          return {ov,wide,broken,dup,ld,cnt,hidden,H:document.body.scrollHeight}}''')
        await pg.screenshot(path=f'{OUT}/{n}-{w}-full.png',full_page=True)
        menu=''
        if w<500:
          await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(300)
          await pg.click('.menu-btn'); await pg.wait_for_timeout(500)
          menu=await pg.evaluate('getComputedStyle(document.querySelector(".mmenu")).visibility')
          if pg_=='index.html': await pg.screenshot(path=f'{OUT}/menu-390.png')
        print(w,pg_,'H',r['H'],'ov',r['ov'],r['wide'],'broken',r['broken'],'dup',r['dup'],'ld',r['ld'],'cnt',r['cnt'],'hidden',r['hidden'],'menu',menu,'errs',errs[:3])
        await ctx.close()
    # reduced motion check
    ctx=await b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
    for pg_ in PAGES:
      pg=await ctx.new_page(); await pg.goto(BASE+pg_,wait_until='load'); await pg.wait_for_timeout(500)
      hid=await pg.evaluate('''()=>[...document.querySelectorAll('main *')].filter(e=>{const s=getComputedStyle(e);return (s.opacity==='0')&&e.getBoundingClientRect().width>0&&!e.closest('.slide,.pin-tip,.lbx')&&!e.classList.contains('go')}).length''')
      lo=await pg.evaluate('!!document.querySelector(".loader")&&getComputedStyle(document.querySelector(".loader")).display!=="none"')
      print('RM',pg_,'hidden',hid,'loader',lo); await pg.close()
    await b.close()
asyncio.run(run())
