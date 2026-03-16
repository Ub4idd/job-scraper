# report.py
import pandas as pd
import os

print("Loading data...")

# 1. Safely locate and load the jobs.csv file we just made
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/final/jobs.csv'))
df = pd.read_csv(csv_path)

print("\n========================================")
print("       JOB MARKET ANALYSIS REPORT       ")
print("========================================")
print(f"Total jobs analyzed: {len(df)}\n")

# 2. Answer Assignment Question: Most common job titles
print("1. Most Common Job Titles:")
print(df['Job title'].value_counts().head(5).to_string())

# 3. Answer Assignment Question: City/region with highest openings
print("\n2. Top Locations:")
print(df['Location'].value_counts().head(3).to_string())

# 4. Answer Assignment Question: Companies posting the highest number of roles
print("\n3. Top Companies Hiring:")
print(df['Company name'].value_counts().head(3).to_string())

# 5. Answer Assignment Question: Count of internship or junior roles
junior_roles = df[df['Job title'].str.contains('Intern|Junior', case=False, na=False)]
print(f"\n4. Count of Internship/Junior roles: {len(junior_roles)}")

# 6. Answer Assignment Question: Top skills
print("\n5. Top Required Skills:")
print(df['Required skills'].value_counts().head(3).to_string())
print("========================================")