import psycopg2
import json

DB_CONFIG = {
    'dbname': 'dsf_2025_poc',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': 5432
}

DEGREE_NAME = 'Computer Science'
COMPLETED = {"CS010A", "CS010B"}


def get_dag(conn, degree_name):
    with conn.cursor() as cur:
        cur.execute("SELECT dag FROM degree_dags WHERE degree_name = %s", (degree_name,))
        row = cur.fetchone()
        return row[0] if row else None

def get_offered_courses(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT subject, course_number FROM courses")
        return {f"{row[0]}{row[1]}" for row in cur.fetchall()}

def recommend_courses(dag, offered, completed):
    eligible = []
    for course, prereqs in dag.items():
        if course not in completed and all(p in completed for p in prereqs):
            if course in offered:
                eligible.append(course)
    return eligible

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    dag = get_dag(conn, DEGREE_NAME)
    if not dag:
        print("Degree not found.")
        return

    offered = get_offered_courses(conn)
    recommended = recommend_courses(dag, offered, COMPLETED)

    print("✅ Recommended Courses for This Quarter:")
    for course in recommended:
        print("-", course)

    conn.close()

if __name__ == "__main__":
    main()
