import sys, asyncio
from playwright.async_api import async_playwright
async def main(itens):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for html, w, h, out in itens:
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.goto(f"file://{html}"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=out, type="jpeg", quality=92); await pg.close()
        await b.close()
import json; asyncio.run(main(json.loads(sys.argv[1])))
