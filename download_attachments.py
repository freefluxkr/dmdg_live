import os
import asyncio
from playwright.async_api import async_playwright

async def main():
    folder = "20261012-1016"
    
    print("==================================================", flush=True)
    print("브라우저 창이 열리면 다시 한번 로그인해 주세요!")
    print("이번에는 게시글 내부에 숨겨진 '실제 첨부파일(HTML 시뮬레이터, PDF 등)'을 다운로드합니다.")
    print("==================================================", flush=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            accept_downloads=True
        )
        page = await context.new_page()
        
        await page.goto("https://nid.naver.com/nidlogin.login")
        
        print("네이버 로그인 창이 열렸습니다.", flush=True)
        print("천천히 로그인 해주세요! (인증번호 입력 등 시간이 오래 걸려도 계속 기다립니다 ⏱️)", flush=True)
        
        # URL에 'nid.naver.com' (네이버 로그인 및 2단계 인증 도메인)이 포함되어 있는 한 무한히 대기합니다.
        while "nid.naver.com" in page.url:
            await asyncio.sleep(1)
            
        print("로그인 완료 감지! 안전한 세션 연결을 위해 3초 대기합니다...", flush=True)
        await asyncio.sleep(3)
        
        for article_id in range(15406, 15425):
            url = f"https://cafe.naver.com/f-e/{article_id}"
            print(f"게시물 {article_id} 첨부파일 탐색 중...", flush=True)
            try:
                await page.goto(url, timeout=15000)
                await page.wait_for_selector('iframe#cafe_main', timeout=10000)
                frame = page.frame_locator('iframe#cafe_main')
                
                # 우측 상단 '첨부파일' 버튼이 있으면 클릭해서 드롭다운 열기
                top_btn = frame.locator('a.button_file')
                if await top_btn.count() > 0:
                    await top_btn.first.click()
                    await page.wait_for_timeout(1000)
                    
                # 다운로드 버튼들 찾기 (본문 내부 '파일 다운로드' 또는 드롭다운 '내PC 저장')
                locators = [
                    frame.locator('a:has-text("파일 다운로드")'),
                    frame.locator('a:has-text("내PC 저장")'),
                    frame.locator('a[href*="CafeFileDown"]')
                ]
                
                downloaded_urls = set()
                
                for loc in locators:
                    count = await loc.count()
                    for i in range(count):
                        elem = loc.nth(i)
                        try:
                            href = await elem.get_attribute('href')
                            if href in downloaded_urls and href is not None: continue
                            if href: downloaded_urls.add(href)
                            
                            async with page.expect_download(timeout=10000) as download_info:
                                await elem.click()
                            download = await download_info.value
                            filename = download.suggested_filename
                            
                            # 고유성을 위해 게시글 ID를 파일명 앞에 붙임
                            save_path = os.path.join(folder, f"{article_id}_{filename}")
                            await download.save_as(save_path)
                            print(f" -> 첨부파일 다운로드 성공: {filename}", flush=True)
                        except Exception as e:
                            pass
            except Exception as e:
                print(f"Error on {article_id}: {e}", flush=True)
                
        await browser.close()
        print("모든 첨부파일(시뮬레이터/PDF) 다운로드 완료!", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
