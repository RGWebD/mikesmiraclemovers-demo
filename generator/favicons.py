import asyncio, os, shutil
from playwright.async_api import async_playwright
from PIL import Image
B=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','brand')); R=os.path.abspath(os.path.join(B,'..'))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':512,'height':512})
        open(f'{B}/_fav.html','w').write('<body style="margin:0;background:transparent"><img src="favicon.svg" style="width:512px;height:512px;display:block"></body>')
        await pg.goto(f'file://{B}/_fav.html'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{B}/favicon-512.png',omit_background=True)
        pg2=await b.new_page(viewport={'width':1200,'height':630})
        html=f'''<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=DM+Sans:wght@700&family=Permanent+Marker&display=swap" rel="stylesheet"><body style="margin:0;width:1200px;height:630px;background:#F6EEDF;position:relative;overflow:hidden">
        <div style="position:absolute;right:40px;top:60px;width:560px;border:4px solid #17140F;border-radius:18px;overflow:hidden;box-shadow:14px 14px 0 #17140F;transform:rotate(-2deg);background:#fff"><div style="background:#17140F;color:#F6EEDF;font:700 15px DM Sans;letter-spacing:3px;padding:10px 16px">FROM: MIKE’S MIRACLE MOVERS</div><img src="file://{R}/img/og-base.jpg" style="width:100%;display:block;height:420px;object-fit:cover"></div>
        <img src="file://{B}/logo-horizontal-light.svg" style="position:absolute;left:50px;top:50px;height:84px">
        <div style="position:absolute;left:54px;top:205px;color:#17140F;font:400 70px/1 'Alfa Slab One';width:560px">Moving day, made to look <span style="font-family:'Permanent Marker';color:#D62F1F;font-size:84px">easy.</span></div>
        <div style="position:absolute;left:0;right:0;bottom:0;background:#D62F1F;color:#fff;border-top:4px solid #17140F;font:400 26px 'Alfa Slab One';padding:16px 54px">★ 4.7 · 354 Google reviews · Jacksonville · (904) 710-1565</div></body>'''
        open(f'{B}/_og.html','w').write(html)
        await pg2.goto(f'file://{B}/_og.html'); await pg2.wait_for_timeout(2500)
        await pg2.screenshot(path=f'{R}/img/og.jpg',type='jpeg',quality=86)
        await b.close()
asyncio.run(main())
im=Image.open(f'{B}/favicon-512.png').convert('RGBA')
for s in (16,32,180): im.resize((s,s),Image.LANCZOS).save(f'{B}/favicon-{s}.png')
im.resize((180,180),Image.LANCZOS).save(f'{R}/apple-touch-icon.png')
im.save(f'{R}/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
shutil.copy(f'{B}/favicon.svg',f'{R}/favicon.svg')
os.remove(f'{B}/_og.html'); os.remove(f'{B}/_fav.html'); print('ok')
