import heapq

prereq_graph = {
    'CS100': [],
    'CS130': ['CS100'],
    'CS201': ['CS130'],
    'CS255': ['CS201'],
    'CS elective': ['CS130']
}

course_priority = {
    'CS100': 1,
    'CS130': 1,
    'CS201': 1,
    'CS255': 1,
    'CS elective': 3
}

completed_courses = {'CS100', 'CS130'}

available_this_quarter = {
    'CS130': {'CRN': 10044, 'time': 'MWF 10–11'},
    'CS201': {'CRN': 10037, 'time': 'TTh 2–3:30'},
    'CS elective': {'CRN': 10107, 'time': 'MWF 1–2'}
}

def get_eligible_courses(prereq_graph, completed, offered, priorities):
    eligible = []
    for course, prereqs in prereq_graph.items():
        if course in completed:
            continue
        if all(p in completed for p in prereqs) and course in offered:
            heapq.heappush(eligible, (priorities.get(course, 99), course))
    return eligible


def main():
    eligible_courses = get_eligible_courses(
        prereq_graph,
        completed_courses,
        available_this_quarter,
        course_priority
    )

    if not eligible_courses:
        print("No eligible courses available this quarter.")
        return

    print("Eligible courses this quarter (by priority):")
    while eligible_courses:
        _, course = heapq.heappop(eligible_courses)
        info = available_this_quarter[course]
        print(f"- {course} (CRN: {info['CRN']}, Time: {info['time']})")

if __name__ == "__main__":
    main()