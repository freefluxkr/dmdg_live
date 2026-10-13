import os
import asyncio
import re
from playwright.async_api import async_playwright

async def main():
    folder = "20261012-1016"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    print("==================================================", flush=True)
    print("브라우저 창이 열리면 네이버에 직접 로그인해 주세요!", flush=True)
    print("로그인 완료 시 자동으로 19개의 게시물 다운로드가 시작됩니다.", flush=True)
    print("==================================================", flush=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        await page.goto("https://nid.naver.com/nidlogin.login")
        print("네이버 로그인 대기 중...", flush=True)
        
        # Wait until URL changes away from nidlogin
        while "nidlogin.login" in page.url:
            await asyncio.sleep(1)
            
        print("로그인 감지됨! 세션을 안정화하기 위해 3초 대기합니다...", flush=True)
        await asyncio.sleep(3)
        print("스크래핑을 시작합니다 🚀", flush=True)
        
        for article_id in range(15406, 15425):
            url = f"https://m.cafe.naver.com/ca-fe/web/cafes/15757610/articles/{article_id}"
            print(f"Fetching {article_id}...", flush=True)
            try:
                await page.goto(url, timeout=15000)
                await page.wait_for_selector('.se-main-container, .post_viewer', timeout=10000)
                
                title = await page.evaluate("document.title")
                title = title.split(' : ')[0]
                
                content_loc = page.locator('.se-main-container, .post_viewer').first
                content = await content_loc.inner_text()
                html_content = await content_loc.inner_html()
                
                safe_title = re.sub(r'[\\/*?:"<>|]', "", title).strip()
                
                md_path = os.path.join(folder, f"{article_id}_{safe_title}.md")
                html_path = os.path.join(folder, f"{article_id}_{safe_title}.html")
                
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n\n{content}")
                    
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(f"<html><head><meta charset='utf-8'><title>{title}</title></head><body><h1>{title}</h1>{html_content}</body></html>")
                print(f"Saved {article_id}: {safe_title}", flush=True)
            except Exception as e:
                print(f"Failed to fetch {article_id}: {e}", flush=True)
        
        await browser.close()
        print("스크래핑 및 파일 다운로드 완료! 브라우저가 닫힙니다.", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
