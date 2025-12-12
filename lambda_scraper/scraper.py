import requests
from selectolax.parser import HTMLParser

BASE_URL = "https://pe.indeed.com/jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
              "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "es-US,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://pe.indeed.com/",
}

def scrape_indeed(query: str, location: str = ""):
    print("Scraping Indeed…")

    params = {
        "q": query,
        "l": location,
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    response.raise_for_status()

    html = HTMLParser(response.text)

    jobs = []

    for card in html.css("div.job_seen_beacon"):
        title = card.css_first("h2 span")
        company = card.css_first(".companyName")
        location = card.css_first(".companyLocation")

        jobs.append({
            "title": title.text(strip=True) if title else None,
            "company": company.text(strip=True) if company else None,
            "location": location.text(strip=True) if location else None,
        })

    return jobs
