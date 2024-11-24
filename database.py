# database.py
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

# Set up a connection to your SQL Server database
def get_db_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.environ['DB_SERVER']};"
        f"DATABASE={os.environ['DB_NAME']};"
        f"UID={os.environ['DB_USER']};"
        f"PWD={os.environ['DB_PASSWORD']}"
    )
    return conn


# Insert jobs into the database
def insert_jobs(jobs):
    conn = get_db_connection()
    cursor = conn.cursor()

    for job in jobs:
        cursor.execute("""
            INSERT INTO jobs (title, company, location, link)
            VALUES (?, ?, ?, ?)
        """, (job['title'], job['company'], job['location'], job['link']))

    conn.commit()
    cursor.close()
    conn.close()


# Get all jobs
def get_all_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    jobs = [
        {"id": row[0], "title": row[1], "company": row[2], "location": row[3], "link": row[4]}
        for row in rows
    ]
    cursor.close()
    conn.close()

    return jobs


# Get a specific job by ID
def get_job_by_id(job_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    row = cursor.fetchone()
    job = {"id": row[0], "title": row[1], "company": row[2], "location": row[3], "link": row[4]}
    cursor.close()
    conn.close()

    return job


# Update a job
def update_job(job_id, title, company, location, link):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET title = ?, company = ?, location = ?, link = ?
        WHERE id = ?
    """, (title, company, location, link, job_id))

    conn.commit()
    cursor.close()
    conn.close()


# Delete a job by ID
def delete_job(job_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))

    conn.commit()
    cursor.close()
    conn.close()

def delete_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs")

    conn.commit()
    cursor.close()
    conn.close()