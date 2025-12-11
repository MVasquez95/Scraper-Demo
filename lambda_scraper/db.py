import os
import psycopg2

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def insert_jobs(jobs):
    conn = connect_db()
    cur = conn.cursor()

    sql = """
    INSERT INTO jobs (job_id, title, company, location, summary, url, scraped_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (job_id) DO NOTHING;
    """

    for job in jobs:
        cur.execute(sql, (
            job["job_id"], job["title"], job["company"],
            job["location"], job["summary"], job["url"],
            job["scraped_at"]
        ))

    conn.commit()
    cur.close()
    conn.close()
