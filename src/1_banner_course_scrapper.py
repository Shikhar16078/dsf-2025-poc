import requests
from requests.cookies import RequestsCookieJar
import time
import json
import os

def get_session_and_headers(term):
    session = requests.Session()
    
    # Step 1: Start session and let it manage cookies
    session.get("https://registrationssb.ucr.edu")
    
    # Step 2: Set headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    # Step 3: POST to establish session
    session.post(
        "https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/term/search?mode=search",
        data={"term": term},
        headers=headers
    )

    return session, headers

def fetch_all_courses(term, headers, session, max_per_request=500):
    courses = []
    pageOffset = 0

    initial_url = (
        f"https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/searchResults/"
        f"searchResults?&txt_term={term}&pageOffset=0&pageMaxSize={max_per_request}&"
        f"sortColumn=subjectDescription&sortDirection=asc"
    )
    response = session.get(initial_url, headers=headers)
    response.raise_for_status()
    total_count = response.json().get("totalCount", 0)

    print(f"Total sections found: {total_count}")

    # Step 6: Loop and fetch
    while len(courses) < total_count:
        print(f"Fetching courses {pageOffset} to {pageOffset + max_per_request}...")
        
        paged_url = (
            f"https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/searchResults/"
            f"searchResults?&txt_term={term}&startDatepicker=&endDatepicker=&"
            f"pageOffset={pageOffset}&pageMaxSize={max_per_request}&"
            f"sortColumn=subjectDescription&sortDirection=asc"
        )

        response = session.get(paged_url, headers=headers)
        response.raise_for_status()
        new_data = response.json().get("data", [])
        
        if not new_data:
            break

        courses.extend(new_data)
        pageOffset += max_per_request

        time.sleep(0.5)  # polite delay to avoid getting rate-limited

    print(f"Fetched {len(courses)} total course sections.")
    return courses

def save_raw_data(courses, output_file="data/raw/raw_courses.json"):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save data
    with open(output_file, "w") as f:
        json.dump(courses, f, indent=2)
    
    print(f"Saved course data to {output_file}")

if __name__ == "__main__":
    term_code = "202440"
    session, headers = get_session_and_headers(term_code)
    courses = fetch_all_courses(term_code, headers, session)
    save_raw_data(courses)