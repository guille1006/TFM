from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        locale="es-ES"
    )
    page = context.new_page()
    page.goto("https://www.idealista.com/venta-viviendas/madrid-madrid/", timeout=60000)
    page.wait_for_timeout(5000)  # Espera 5 seg
    html = page.content()
    print(html[:1000])  # Verifica si ves anuncios o el iframe CAPTCHA
    browser.close()

