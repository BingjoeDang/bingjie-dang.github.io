import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

SCHOLAR_URL = 'https://scholar.google.com/citations?user=Mfp83rUAAAAJ&hl=en'
OUTPUT = Path('/mnt/data/citations.json')


def norm(text: str) -> str:
    text = (text or '').strip().lower()
    text = re.sub(r'\s+', ' ', text)
    return text


def key_for(title: str) -> str:
    title = norm(title)
    title = re.sub(r'[^a-z0-9]+', '-', title)
    return title.strip('-')


def scrape_all_publications():
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(SCHOLAR_URL, wait_until='domcontentloaded', timeout=120000)
        page.wait_for_selector('#gsc_a_b .gsc_a_tr', timeout=120000)

        last_count = -1
        while True:
            current = page.locator('#gsc_a_b .gsc_a_tr').count()
            if current == last_count:
                break
            last_count = current
            more = page.locator('#gsc_bpf_more')
            disabled = more.get_attribute('disabled')
            if disabled is not None:
                break
            more.click()
            page.wait_for_timeout(1200)

        for row in page.locator('#gsc_a_b .gsc_a_tr').all():
            title = row.locator('.gsc_a_at').inner_text().strip()
            cited_by = row.locator('.gsc_a_c a').inner_text().strip()
            year = row.locator('.gsc_a_y').inner_text().strip()
            citations = int(cited_by) if cited_by.isdigit() else 0
            rows.append({
                'key': key_for(title),
                'title': title,
                'citations': citations,
                'year': year,
            })

        browser.close()
    return rows


if __name__ == '__main__':
    data = scrape_all_publications()
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Wrote {len(data)} records to {OUTPUT}')
