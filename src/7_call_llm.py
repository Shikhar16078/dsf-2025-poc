import requests

GEMINI_API_KEY = "API_KEY_HERE"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def ask_gemini_schedule_recommendation(eligible_courses):
    course_list_text = "\n".join([f"- {subject} {course_number}" for _, subject, course_number in eligible_courses])
    
    prompt = f"""
I am a computer science student. These are the courses I'm eligible to take this quarter:

{course_list_text}

Please help me build a suggested schedule using 3–5 of these classes. I prefer a balanced workload and want to satisfy core requirements first. Please explain your choices briefly.
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt.strip()}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(GEMINI_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        reply = data['candidates'][0]['content']['parts'][0]['text']
        return reply
    else:
        raise Exception(f"Gemini API Error: {response.status_code} - {response.text}")


if __name__ == "__main__":
    eligible_courses = [
        ("12345", "CS", "141"),
        ("12346", "CS", "150"),
        ("12347", "STAT", "155"),
        ("12348", "MATH", "010A"),
        ("12349", "PHYS", "040A")
    ]

    response_text = ask_gemini_schedule_recommendation(eligible_courses)
    print(response_text)