# scraper.py
import requests
from bs4 import BeautifulSoup
import brotli

def scrape_jobs():
    url = 'https://remoteok.com/remote-jobs'
    headers = {
        "Host": "remoteok.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://remoteok.com/remote-jobs",
        "Cookie": "ref=https%3A%2F%2Fwww.google.com%2F; adShuffler=0; new_user=true; visit_count=4",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin"
    }

    # Request the URL
    resp = requests.get(url, headers=headers)

    # Decode the response based on Content-Encoding
    resp_text = None
    try:
        if 'br' in resp.headers.get('Content-Encoding', ''):
            resp_text = brotli.decompress(resp.content).decode('utf-8')
            print("Successfully decompressed Brotli content.")
        else:
            resp_text = resp.text
            print("No Brotli encoding detected; using raw response text.")
    except brotli.error as e:
        print(f"Brotli decompression failed: {e}")
        print("Falling back to raw response text.")
        resp_text = resp.text

    # Parse the HTML
    soup = BeautifulSoup(resp_text, "html.parser")

    # Extract job postings
    jobs = []
    for job_elem in soup.select(".job"):
        try:
            title = job_elem.select_one(".company_and_position [itemprop='title']").text.strip()
            company = job_elem.select_one("[itemprop='name']").text.strip()
            location = job_elem.select_one(".location").text.strip() if job_elem.select_one(".location") else "Remote"
            link = "https://remoteok.com" + job_elem.select_one(".preventLink")["href"]
            jobs.append({"title": title, "company": company, "location": location, "link": link})
        except AttributeError:
            continue

    return jobs

# from database import insert_jobs
#
# if __name__ == "__main__":
#     jobs = scrape_jobs()
#     print(f"Scraped {len(jobs)} jobs.")
#     insert_jobs(jobs)
#     print("Jobs successfully inserted into the database!")

