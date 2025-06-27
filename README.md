# Data Science Fellowship 2025 – Schedule Planning Chatbot (POC)

This project is a proof-of-concept chatbot to help students generate valid, personalized course schedules based on their degree plan and completed coursework.

---

## ✅ Current Progress

### 🔹 1. Extract: Fetch Course Data from Banner API
- Pulled raw course section data from UCR’s Banner API (Fall 2024 – `term=202440`)
- Saved raw JSON to: `data/raw/raw_courses.json`

### 🔹 2. Transform: Clean & Normalize Using PySpark
- Parsed nested JSON into structured 3NF tables using PySpark
- Output tables:
  - `courses.csv`
  - `sections.csv`
  - `instructors.csv`
  - `meeting_times.csv`
- Saved all files in: `data/cleaned/`

### 🔹 3. Load: Push into PostgreSQL (via Docker)

#### 🐳 Pull the Official Postgres Image (if not already installed)

```bash
docker pull postgres
```

Command used to create a local Postgres container with preconfigured database:
```bash
docker run --name dsf2025-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=dsf_2025_poc \
  -p 5432:5432 \
  -d postgres
```

Data was loaded into this database using a Python script (`3_course_to_postgres.py`) powered by `pandas` + `sqlalchemy`.

---

## 🧪 Example Query

Query to return all **graduate-level CS courses** offered in **Fall 2024**:

```sql
SELECT * FROM public.courses
WHERE subject = 'CS' AND course_number LIKE '2%';
```
<img src="media/images/grad-courses.png" alt="Graduate CS Courses Demo" width="600"/>

---

## 🔜 Next Steps

- Create student mock profiles (completed courses + degree plan)
- Build a scheduling engine (prerequisite checking, conflict avoidance)
- Wrap logic in a chatbot interface (e.g., Streamlit or Flask)
- Support real-time course updates (optionally rerun fetchers per quarter)

---

## 📂 Folder Structure

```
data/
├── raw/                 # Raw JSON from Banner API
├── cleaned/             # Cleaned CSVs
src/
├── fetch_courses.py     # Banner API fetcher
├── clean_courses.py     # PySpark transformer
├── load_to_postgres.py  # CSV → PostgreSQL loader
```

---

> 💡 Tip: Adjust DB credentials and port in scripts if needed for your environment.