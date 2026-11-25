import asyncio, sys, os
from playwright.async_api import async_playwright
from PIL import Image
url,tag,w=sys.argv[1],sys.argv[2],int(sys.argv[3]); out='/workspace/mmm-work/'+tag; os.makedirs(out,exist_ok=True)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    ctx=await b.new_context(viewport={'width':w,'height':900 if w>500 else 844},device_scale_factor=1,is_mobile=w<500,has_touch=w<500)
    pg=await ctx.new_page(); await pg.goto(url,wait_until='load'); await pg.wait_for_timeout(2600)
    H=await pg.evaluate('document.body.scrollHeight'); y=0
    while y<H: y+=400; await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(90)
    await pg.wait_for_timeout(1800); await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(600)
    await pg.screenshot(path=out+'/full.png',full_page=True); await b.close()
  im=Image.open(out+'/full.png'); H=im.height; step=1600 if w>500 else 1700; i=0
  for y in range(0,H,step):
    im.crop((0,y,im.width,min(H,y+step))).save(f'{out}/s{i:02d}.png'); i+=1
  print(H,i)
asyncio.run(m())
