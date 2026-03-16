import pandas as pd
import matplotlib.pyplot as plt
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, '../data/final/jobs.csv')

print("Loading data...")
df = pd.read_csv(csv_path)

# Print Text Metrics
entry_level_roles = df[df['Job title'].str.contains('Junior|Intern|Entry|Early', case=False, na=False)]
print("\n--- WORKFORCE ANALYSIS REPORT ---")
print(f"Total Entry-Level/Intern Roles Found: {len(entry_level_roles)}")
print("\nTop Hiring Companies in Dataset:")
print(df['Company name'].value_counts().head(5).to_string())
print("\nTop 3 Most Common Job Titles:")
print(df['Job title'].value_counts().head(3).to_string())

# Generate Charts
# Chart 1: Titles
plt.figure(figsize=(10, 6))
df['Job title'].value_counts().head(5).plot(kind='barh', color='#ff4500')
plt.title('Top 5 Job Titles')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'chart_top_titles.png'))
plt.close()

# Chart 2: Locations
plt.figure(figsize=(8, 8))
df['Location'].value_counts().head(5).plot(kind='pie', autopct='%1.1f%%')
plt.title('Top Hiring Locations')
plt.ylabel('')
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'chart_locations.png'))
plt.close()

# Chart 3: Skills
all_skills = df['Required skills'].dropna().str.split(', ').sum()
skill_counts = pd.Series(all_skills).value_counts().head(5)
plt.figure(figsize=(10, 6))
skill_counts.plot(kind='bar', color='#1e90ff')
plt.title('Most In-Demand Tech Skills')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'chart_top_skills.png'))
plt.close()

print("\nSuccess! Check your 'analysis' folder for the 3 PNG charts.")