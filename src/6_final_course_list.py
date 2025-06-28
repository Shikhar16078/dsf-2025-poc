import psycopg2
from queue import PriorityQueue

def get_eligible_courses(student_id):

    conn = psycopg2.connect(
        dbname="dsf_2025_poc", user="postgres", password="password", host="localhost", port=5432
    )
    cur = conn.cursor()

    cur.execute("SELECT degree, courses_taken FROM students WHERE student_id = %s", (student_id,))
    row = cur.fetchone()
    if not row:
        raise ValueError("Student not found.")
    degree_name, courses_taken = row
    completed_courses = set(courses_taken)

    cur.execute("SELECT dag FROM degree_dags WHERE degree_name = %s", (degree_name,))
    dag_json = cur.fetchone()[0]
    dag = dag_json

    pq = PriorityQueue()
    for course_code, prereqs in dag.items():
        if not prereqs or all(pr in completed_courses for pr in prereqs):
            pq.put((0, course_code)) 

    cur.execute("SELECT course_id, subject, course_number FROM courses")
    offered_courses = cur.fetchall()

    offered_codes = {
        f"{subject}{course_number}".replace(" ", "") for _, subject, course_number in offered_courses
    }

    eligible_courses = []
    while not pq.empty():
        _, course_code = pq.get()
        if course_code in offered_codes:
            for course_id, subject, course_number in offered_courses:
                if course_code == f"{subject}{course_number}".replace(" ", ""):
                    eligible_courses.append((course_id, subject, course_number))

    cur.close()
    conn.close()
    return eligible_courses

if __name__ == "__main__":
    student_id = 1
    print(get_eligible_courses(student_id))
