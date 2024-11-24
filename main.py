# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from scraper import scrape_jobs
from database import insert_jobs, get_all_jobs, get_job_by_id, update_job, delete_job, delete_jobs
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Pydantic model for job data validation
class Job(BaseModel):
    title: str
    company: str
    location: str
    link: str


@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/scrape")
def scrape_and_store():
    # Scrape jobs
    jobs = scrape_jobs()

    # Insert jobs into the database
    insert_jobs(jobs)

    return {"message": "Jobs have been scraped and stored in the database."}


@app.get("/jobs")
def read_jobs():
    # Get all jobs from the database
    jobs = get_all_jobs()
    return {"jobs": jobs}


@app.get("/jobs/{job_id}")
def read_job(job_id: int):
    # Get a specific job by ID
    job = get_job_by_id(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job": job}


@app.put("/jobs/{job_id}")
def update_job_info(job_id: int, job: Job):
    # Update a job's information
    updated = update_job(job_id, job.title, job.company, job.location, job.link)
    if updated == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job updated successfully"}


@app.delete("/jobs/{job_id}")
def delete_job_info(job_id: int):
    # Delete a job by ID
    deleted = delete_job(job_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}

@app.delete("/delete_jobs")
def delete_all_jobs():

    delete_jobs()

    return {"message": "all jobs deleted"}
