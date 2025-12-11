import requests
from selectolax.parser import HTMLParser
from datetime import datetime

def scrape_indeed(keyword="python developer", location=""):

    query = keyword.replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={query}&l={location}"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    html = HTMLParser(response.text)
    jobs = []

    for div in html.css("div.cardOutline"):
        try:
            job_id = div.attributes.get("data-jk")
            if not job_id:
                continue

            title = div.css_first("h2.jobTitle span").text()
            company = div.css_first("span.companyName").text() if div.css_first("span.companyName") else None
            location = div.css_first("div.companyLocation").text() if div.css_first("div.companyLocation") else None
            summary = div.css_first("div.job-snippet").text(separator=" ").strip() if div.css_first("div.job-snippet") else None
            
            job_url = f"https://www.indeed.com/viewjob?jk={job_id}"

            jobs.append({
                "job_id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "summary": summary,
                "url": job_url,
                "scraped_at": datetime.utcnow()
            })
        except Exception:
            pass

    return jobs
