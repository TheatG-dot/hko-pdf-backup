import asyncio
from playwright.async_api import async_playwright
import datetime

async def save_pdf():
    async with async_playwright() as p:
        # 啟動瀏覽器
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # 確保網址是純文字字串，嚴禁包含方括號或小括號
        url = "https://www.hko.gov.hk/en/wxinfo/ts/tsarchive/wxinfo_24hrs.shtml"
        
        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(5) # 等待數據圖表渲染完成
        
        # 時區校正：將 UTC 轉為香港時間 (UTC+8)
        hk_time = datetime.datetime.now() + datetime.timedelta(hours=8)
        now_str = hk_time.strftime("%Y-%m-%d_%H-%M")
        filename = f"HKO_24hrs_{now_str}.pdf"
        
        # 輸出為 PDF
        await page.pdf(path=filename, format="A4", print_background=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(save_pdf())
