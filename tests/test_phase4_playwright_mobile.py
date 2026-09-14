# -*- coding: utf-8 -*-
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def run_playwright_mobile_e2e():
    print("==================================================")
    print("=== PLAYWRIGHT MOBILE E2E COMPREHENSIVE TEST ===")
    print("==================================================")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Emulate iPhone 14 / Pixel 7 mobile viewport
        context = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True
        )
        page = await context.new_page()

        url = "http://localhost:8080/mobile_antigravity.html"
        print(f"1. Navigating to {url}...")
        await page.goto(url, wait_until="networkidle")

        # Check telemetry pill
        await page.wait_for_timeout(2000)
        pill_text = await page.locator("#malecns-pill-text").inner_text()
        print(f"2. Verified Live Telemetry Pill: '{pill_text}'")
        assert "MaleCNS 166k" in pill_text, f"Unexpected pill text: {pill_text}"

        # Tab 1: Check plan title and button
        plan_title = await page.locator("#plan-title-text").inner_text()
        print(f"3. Verified Tab 1 Plan Title: '{plan_title}'")
        assert "Plan:" in plan_title

        # Switch to Tab 2: Code & Diff
        print("4. Switching to Tab 2 (Code & Diff)...")
        await page.click("div.nav-item[onclick*=\"diff\"]")
        await page.wait_for_timeout(800)
        diff_pane_visible = await page.locator("#pane-diff").is_visible()
        print(f"   Tab 2 Diff Pane Visible: {diff_pane_visible}")
        assert diff_pane_visible is True

        # Switch to Tab 3: Preview & Log
        print("5. Switching to Tab 3 (Preview & Log)...")
        await page.click("div.nav-item[onclick*=\"preview\"]")
        await page.wait_for_timeout(800)
        preview_pane_visible = await page.locator("#pane-preview").is_visible()
        print(f"   Tab 3 Preview Pane Visible: {preview_pane_visible}")
        assert preview_pane_visible is True

        # Capture final E2E mobile screenshot
        out_path = OUTPUT_DIR / "screen_phase4_mobile_e2e_complete.png"
        await page.screenshot(path=str(out_path), full_page=False)
        print(f"6. Captured mobile screenshot: {out_path} ({os.path.getsize(out_path)} bytes)")

        # Also copy to artifacts directory if available
        artifact_dir = Path(r"C:\Users\magic\.gemini\antigravity\brain\884686c1-bc24-45ed-9bc8-5a7e26d0aee1")
        if artifact_dir.exists():
            import shutil
            shutil.copy2(out_path, artifact_dir / "screen_phase4_mobile_e2e_complete.png")

        await browser.close()

    print("--------------------------------------------------")
    print(">>> PLAYWRIGHT MOBILE E2E VERIFIED (100% PASS) <<<")
    print("--------------------------------------------------")

if __name__ == "__main__":
    asyncio.run(run_playwright_mobile_e2e())
