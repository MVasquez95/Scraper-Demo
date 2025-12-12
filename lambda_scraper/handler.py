from scraper import scrape_computrabajo
from db import insert_jobs

def lambda_handler(event, context):
    query = event.get("query", "python developer")
    save_to_db = event.get("save_to_db", True)
    pages = int(event.get("pages", 1))  # cantidad de páginas a scrapear

    jobs = scrape_computrabajo(query, max_pages=pages)

    if save_to_db and jobs:
        insert_jobs(jobs)

    return {
        "statusCode": 200,
        "body": {
            "jobs_count": len(jobs),
            "jobs": jobs[:3]  # mostramos solo 3 para no llenar el log
        }
    }