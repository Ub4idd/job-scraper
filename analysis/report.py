import pandas as pd
import matplotlib.pyplot as plt
import os

print("Starting Data Analysis...")

# 1. Set up paths to read data and save images
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, '../data/final/jobs.csv')

# Check if file exists
if not os.path.exists(csv_path):
    print(f"Error: Could not find data file at {csv_path}")
    exit()

df = pd.read_csv(csv_path)

# --- TERMINAL REPORT ---
print("\n" + "="*30)
print("🎯 HIRING INSIGHTS REPORT")
print("="*30)

total_jobs = len(df)
print(f"Total Jobs Analyzed: {total_jobs}")

# Company Breakdown
print("\n🏢 Jobs by Company:")
company_counts = df['Company name'].value_counts()
print(company_counts.to_string())

# Entry-Level & Internship Tracker
entry_level_roles = df[df['Job title'].str.contains('Junior|Intern|Entry|Early|Associate', case=False, na=False)]
print(f"\n🌱 Entry-Level & Internship Roles Found: {len(entry_level_roles)}")

print("\nGenerating visual charts...")

# --- GENERATE PNG IMAGES ---

# Chart 1: Jobs by Company (Proves your scraper hit all 3 targets)
plt.figure(figsize=(8, 6))
company_counts.plot(kind='bar', color=['#FF4500', '#F24E1E', '#58CC02']) # Reddit, Figma, Duolingo colors
plt.title('Job Openings by Company', fontsize=14, fontweight='bold')
plt.ylabel('Number of Openings')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'chart_1_companies.png'))
plt.close()

# Chart 2: Top 10 Job Titles
plt.figure(figsize=(10, 6))
df['Job title'].value_counts().head(10).sort_values().plot(kind='barh', color='skyblue')
plt.title('Top 10 Most Frequent Job Titles', fontsize=14, fontweight='bold')
plt.xlabel('Number of Openings')
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'chart_2_top_titles.png'))
plt.close()

# Chart 3: Top Hiring Locations
plt.figure(figsize=(10, 6))
df['Location'].value_counts().head(10).sort_values().plot(kind='barh', color='lightcoral')
plt.title('Top 10 Hiring Locations', fontsize=14, fontweight='bold')
plt.xlabel('Number of Openings')
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'chart_3_locations.png'))
plt.close()

# Chart 4: Most In-Demand Skills
# We split the comma-separated strings to count individual skills properly
all_skills = df['Required skills'].dropna().str.split(', ').explode()
# Filter out the fallback 'General Skills' to focus on actual tech
tech_skills = all_skills[all_skills != 'General Technical Skills']
skill_counts = tech_skills.value_counts().head(10)

plt.figure(figsize=(10, 6))
skill_counts.plot(kind='bar', color='mediumseagreen')
plt.title('Most In-Demand Technical Skills', fontsize=14, fontweight='bold')
plt.ylabel('Frequency in Job Descriptions')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'chart_4_top_skills.png'))
plt.close()

print("✅ Success! 4 analysis images saved in the /analysis folder.")