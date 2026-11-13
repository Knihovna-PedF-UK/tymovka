#!/usr/bin/python
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess


URL = (
    "https://pages.pedf.cuni.cz/studovna/"
    "wp-admin/admin.php?page=booked-settings"
)

PROFILE_DIR = Path.home() / ".local/share/studovna-browser"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    async with async_playwright() as p:
        # Trvalý profil prohlížeče – uchovává cookies.
        context = await p.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            headless=False,
        )

        page = await context.new_page()
        await page.goto(URL)

        print("Pokud je potřeba, přihlas se přes CAS.")
        input("Po přihlášení stiskni Enter...")

        # Export pomocí cookies z přihlášeného prohlížeče.
        response = await page.request.post(
            URL,
            form={
                "appointment_time": "",
                "appointment_type": "any",
                "booked_export_appointments_csv": "1",
            },
        )

        if response.ok:
            data = await response.body()
            SCRIPT_DIR = Path(__file__).resolve().parent
            Path("appointments.csv").write_bytes(data)
            print(f"Staženo: {len(data)} bajtů")
            subprocess.run(
              ["texlua", str(SCRIPT_DIR / "tymovka-print"),
               str(Path("appointments.csv").resolve())],
               check=True,
            )
        else:
            print("Chyba:", response.status)

        await context.close()

asyncio.run(main())
