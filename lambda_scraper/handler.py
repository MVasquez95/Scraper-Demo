from scraper import scrape_indeed
from db import insert_jobs

def lambda_handler(event, context):
    print("Scraping Indeed…")
    
    jobs = scrape_indeed("python developer")

    print(f"Jobs found: {len(jobs)}")

    if jobs:
        insert_jobs(jobs)

    return {
        "statusCode": 200,
        "body": f"Inserted {len(jobs)} jobs"
    }