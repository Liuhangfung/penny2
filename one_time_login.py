#!/usr/bin/env python3
"""
One-time QR code login script
This will open a browser, let you scan the QR code, and save cookies
Run this ONCE on the server, then switch to cookie-based login
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from playwright.async_api import async_playwright
import config


async def main():
    print("=" * 60)
    print("MediaCrawler - One-Time QR Login")
    print("=" * 60)
    print("\n🔧 This will:")
    print("  1. Open a browser window")
    print("  2. Show QR code for you to scan")
    print("  3. Save cookies after successful login")
    print("  4. Exit\n")
    print("After this, you can switch to cookie-based login!")
    print("=" * 60)
    
    async with async_playwright() as playwright:
        # Launch browser (NOT headless)
        print("\n🚀 Launching browser...")
        browser = await playwright.chromium.launch(
            headless=False,  # Must be False to see the browser
            channel="chromium"
        )
        
        # Create context
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        # Create page
        page = await context.new_page()
        
        # Go to XiaoHongShu
        print("📱 Opening XiaoHongShu...")
        await page.goto("https://www.xiaohongshu.com")
        await page.wait_for_timeout(2000)
        
        # Click login button
        print("🔑 Clicking login button...")
        try:
            await page.click("text=登录", timeout=5000)
        except:
            # Try alternative selectors
            try:
                await page.click(".login-btn", timeout=5000)
            except:
                print("⚠️  Could not find login button, please click it manually")
        
        await page.wait_for_timeout(2000)
        
        # Wait for QR code to appear
        print("\n📸 QR CODE SHOULD NOW BE VISIBLE IN THE BROWSER")
        print("=" * 60)
        print("👉 PLEASE SCAN THE QR CODE WITH YOUR PHONE NOW!")
        print("=" * 60)
        
        # Wait for login success (URL change or specific element)
        print("\n⏳ Waiting for you to scan the QR code...")
        print("   (This will wait up to 120 seconds)\n")
        
        try:
            # Wait for redirect to homepage after login
            await page.wait_for_url("**/explore**", timeout=120000)
            print("\n✅ LOGIN SUCCESSFUL!")
            
        except:
            # Alternative: wait for specific element that appears after login
            try:
                await page.wait_for_selector(".avatar", timeout=120000)
                print("\n✅ LOGIN SUCCESSFUL!")
            except:
                print("\n❌ Login timed out. Please try again.")
                await browser.close()
                return
        
        # Save cookies
        print("\n💾 Saving cookies...")
        cookies_dir = SCRIPT_DIR / "cookies"
        cookies_dir.mkdir(exist_ok=True)
        
        cookies = await context.cookies()
        
        # Save cookies in the format MediaCrawler expects
        import json
        cookie_file = cookies_dir / "xiaohongshu.json"
        
        with open(cookie_file, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Cookies saved to: {cookie_file}")
        
        await page.wait_for_timeout(3000)
        await browser.close()
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Setup complete!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("  1. Edit config/base_config.py")
        print("     Change: LOGIN_TYPE = \"cookie\"")
        print("  2. Restart your web app")
        print("  3. Create jobs - they will use saved cookies!")
        print("\n✨ No more QR code scanning needed!\n")


if __name__ == "__main__":
    asyncio.run(main())

