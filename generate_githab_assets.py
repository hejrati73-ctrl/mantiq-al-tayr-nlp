import pandas as pd

net_v2 = pd.read_csv('final_network_analysis_v2_en.csv')
turning_points = pd.read_csv('structural_turning_points.csv')
persistence = pd.read_csv('concept_persistence.csv')
pmi = pd.read_csv('pmi_analysis_en.csv')

summary_md = f"""# Mantiq al-Tayr: Computational Text & Network Analysis

## 1. Network Macro Metrics (V2 Baseline)
{net_v2.to_markdown(index=False)}

## 2. Structural Turning Points
{turning_points.to_markdown(index=False)}

## 3. Concept Persistence Classification
{persistence[['Concept', 'Classification', 'Presence_Count']].to_markdown(index=False)}

## 4. Statistically Significant PMI Word Pairs
{pmi.to_markdown(index=False)}
"""

with open('PROJECT_SUMMARY.md', 'w', encoding='utf-8') as f:
    f.write(summary_md)

print("Successfully generated: PROJECT_SUMMARY.md")