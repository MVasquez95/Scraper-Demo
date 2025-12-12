from scraper import scrape_indeed
from db import insert_jobs

def lambda_handler(event, context):
    query = event.get("query", "python developer")
    save_to_db = event.get("save_to_db", True)
    
    jobs = scrape_indeed(query)

    if save_to_db and jobs:
        insert_jobs(jobs)

    return {
        "statusCode": 200,
        "body": {"jobs_count": len(jobs), "jobs": jobs}
    }
