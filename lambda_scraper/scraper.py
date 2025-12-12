import requests
from selectolax.parser import HTMLParser
from datetime import datetime
import time

BASE_URL = "https://www.computrabajo.com.pe/buscar"
JOB_BASE_URL = "https://www.computrabajo.com.pe"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def scrape_job_detail(url: str) -> dict:
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        html = HTMLParser(response.text)

        desc_block = html.css_first(".box_detail")
        description = desc_block.text(strip=True) if desc_block else None

        date_block = html.css_first(".box_detail > div > span")
        posted_at = None
        if date_block:
            text = date_block.text(strip=True)

            # ejemplo: "Publicado hace 2 días"
            if "hace" in text:
                posted_at = datetime.now()
            else:
                posted_at = None

        return {
            "description": description,
            "posted_at": posted_at
        }

    except Exception as e:
        print(f"Error scraping detail for {url}: {e}")
        return {"description": None, "posted_at": None}


def scrape_computrabajo(query: str, max_pages: int = 1):
    jobs = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}…")

        params = {
            "q": query.replace(" ", "-"),
            "p": page
        }

        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()

        html = HTMLParser(response.text)

        cards = html.css("article.box_offer")

        if not cards:
            print("No more results.")
            break

        for card in cards:
            title_el = card.css_first("a")
            company_el = card.css_first(".it-logos")
            location_el = card.css_first(".it-location")
            salary_el = card.css_first(".tag-base-salary")

            url = title_el.attributes.get("href") if title_el else None
            if url:
                full_url = JOB_BASE_URL + url
            else:
                full_url = None

            # scrap detail
            detail = scrape_job_detail(full_url) if full_url else {}

            jobs.append({
                "title": title_el.text(strip=True) if title_el else None,
                "company": company_el.text(strip=True) if company_el else None,
                "location": location_el.text(strip=True) if location_el else None,
                "salary": salary_el.text(strip=True) if salary_el else None,
                "url": full_url,
                "source": "computrabajo",
                "description": detail.get("description"),
                "posted_at": detail.get("posted_at")
            })

            # dormir 0.5s por cortesía
            time.sleep(0.5)

    return jobs
