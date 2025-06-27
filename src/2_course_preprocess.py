from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode_outer, concat_ws, monotonically_increasing_id, when, lit
import os

# Initialize Spark
spark = SparkSession.builder.appName("CleanBannerCourses").getOrCreate()

# Load raw course JSON
df = spark.read.option("multiline", "true").json("data/raw/raw_courses.json")

# -----------------------------
# 1. Courses Table (3NF)
# -----------------------------
courses_df = df.select(
    col("subject"),
    col("courseNumber").alias("course_number"),
    col("courseTitle").alias("title")
).dropDuplicates()

# Add surrogate primary key
courses_df = courses_df.withColumn("course_id", monotonically_increasing_id())

# Save for joining
courses_df.cache()

# Rename courseNumber to course_number for join compatibility
df = df.withColumnRenamed("courseNumber", "course_number")

# -----------------------------
# 2. Sections Table
# -----------------------------
# Join back to raw data to get course_id
df = df.join(courses_df, on=["subject", "course_number"], how="left")

sections_df = df.select(
    col("courseReferenceNumber").alias("crn"),
    col("term"),
    col("course_id"),
    col("creditHourLow").alias("credits"),
    col("openSection").alias("is_open"),
    col("maximumEnrollment").alias("max_enrollment"),
    col("enrollment"),
    col("seatsAvailable").alias("seats_available"),
    col("waitCapacity").alias("wait_capacity"),
    col("waitCount").alias("wait_count"),
    col("instructionalMethodDescription").alias("instruction_mode")
).dropDuplicates(["crn"])

# -----------------------------
# 3. Instructors Table
# -----------------------------
instructors_df = df.select(
    col("courseReferenceNumber").alias("crn"),
    explode_outer("faculty").alias("faculty")
).select(
    col("crn"),
    col("faculty.displayName").alias("name"),
    col("faculty.emailAddress").alias("email")
).dropna(subset=["name"]).dropDuplicates(["crn", "email"])

# -----------------------------
# 4. Meeting Times Table
# -----------------------------
meetings_df = df.select(
    col("courseReferenceNumber").alias("crn"),
    explode_outer("meetingsFaculty").alias("meeting")
).select(
    col("crn"),
    col("meeting.meetingTime.beginTime").alias("start_time"),
    col("meeting.meetingTime.endTime").alias("end_time"),
    col("meeting.meetingTime.buildingDescription").alias("building"),
    col("meeting.meetingTime.room").alias("room"),
    col("meeting.meetingTime.monday"),
    col("meeting.meetingTime.tuesday"),
    col("meeting.meetingTime.wednesday"),
    col("meeting.meetingTime.thursday"),
    col("meeting.meetingTime.friday")
)

# Create days string
meetings_df = meetings_df.withColumn(
    "days",
    concat_ws("",
        when(col("monday"), "M").otherwise(""),
        when(col("tuesday"), "T").otherwise(""),
        when(col("wednesday"), "W").otherwise(""),
        when(col("thursday"), "R").otherwise(""),
        when(col("friday"), "F").otherwise("")
    )
).drop("monday", "tuesday", "wednesday", "thursday", "friday") \
 .dropDuplicates(["crn", "start_time", "end_time", "building", "room", "days"])

import os
import shutil
import glob

# -----------------------------
# 5. Save All as CSVs
# -----------------------------
output_base = "data/cleaned"

# Clear existing data
if os.path.exists(output_base):
    shutil.rmtree(output_base)
os.makedirs(output_base, exist_ok=True)

def write_and_rename(df, subfolder, filename):
    tmp_path = os.path.join(output_base, subfolder)
    df.coalesce(1).write.option("header", True).mode("overwrite").csv(tmp_path)

    # Find the actual part file
    part_file = glob.glob(os.path.join(tmp_path, "part-*.csv"))[0]
    final_path = os.path.join(output_base, filename)

    # Move and rename
    shutil.move(part_file, final_path)
    shutil.rmtree(tmp_path)
    print(f"Saved {filename}")

# Save each table
write_and_rename(courses_df.select("course_id", "subject", "course_number", "title"), "tmp_courses", "courses.csv")
write_and_rename(sections_df, "tmp_sections", "sections.csv")
write_and_rename(instructors_df, "tmp_instructors", "instructors.csv")
write_and_rename(meetings_df, "tmp_meetings", "meeting_times.csv")

print("Cleaned and renamed CSVs saved to: data/cleaned/")

# Stop Spark
spark.stop()
