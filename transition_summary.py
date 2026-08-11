import csv
from collections import defaultdict

input_file = "transition_analysis.csv"
output_file = "transition_summary.csv"

data = defaultdict(list)

# ==========================================
# READ TRANSITION DATA
# ==========================================

with open(input_file, "r", encoding="utf-8-sig") as f:

    reader = csv.DictReader(f)

    for row in reader:

        data[row["Transition"]].append({
            "Concept_A": row["Concept_A"],
            "Concept_B": row["Concept_B"],
            "Change": float(row["Change"]),
            "Absolute_Change": float(row["Absolute_Change"])
        })


# ==========================================
# ANALYZE EACH TRANSITION
# ==========================================

summary = []

for transition, rows in data.items():

    # Strongest emerging relationships
    emerging = sorted(
        rows,
        key=lambda x: x["Change"],
        reverse=True
    )[:10]

    # Strongest declining relationships
    declining = sorted(
        rows,
        key=lambda x: x["Change"]
    )[:10]

    print()
    print("=" * 75)
    print(transition)
    print("=" * 75)

    print()
    print("TOP EMERGING RELATIONSHIPS")
    print("-" * 75)

    for row in emerging:

        print(
            f"{row['Concept_A']} -- {row['Concept_B']} | "
            f"Change: {row['Change']:+.4f}"
        )

    print()
    print("TOP DECLINING RELATIONSHIPS")
    print("-" * 75)

    for row in declining:

        print(
            f"{row['Concept_A']} -- {row['Concept_B']} | "
            f"Change: {row['Change']:+.4f}"
        )

    # Save top 10 emerging
    for rank, row in enumerate(emerging, 1):

        summary.append({
            "Transition": transition,
            "Direction": "Emerging",
            "Rank": rank,
            "Concept_A": row["Concept_A"],
            "Concept_B": row["Concept_B"],
            "Change": round(row["Change"], 6)
        })

    # Save top 10 declining
    for rank, row in enumerate(declining, 1):

        summary.append({
            "Transition": transition,
            "Direction": "Declining",
            "Rank": rank,
            "Concept_A": row["Concept_A"],
            "Concept_B": row["Concept_B"],
            "Change": round(row["Change"], 6)
        })


# ==========================================
# SAVE SUMMARY
# ==========================================

fieldnames = [
    "Transition",
    "Direction",
    "Rank",
    "Concept_A",
    "Concept_B",
    "Change"
]

with open(
    output_file,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(summary)


# ==========================================
# COMPLETE
# ==========================================

print()
print("=" * 75)
print("TRANSITION SUMMARY COMPLETE")
print("=" * 75)

print("Created:", output_file)