import csv

input_file = "normalized_edge_evolution_long.csv"
output_file = "transition_analysis.csv"

stages = [
    "Opening",
    "Birds_Journey",
    "Seven_Valleys",
    "Simurgh_Encounter",
    "Final_State"
]

data = {}

# ==========================================
# READ NORMALIZED EDGE DATA
# ==========================================

with open(input_file, "r", encoding="utf-8-sig") as f:

    reader = csv.DictReader(f)

    for row in reader:

        edge = tuple(sorted([
            row["Concept_A"],
            row["Concept_B"]
        ]))

        stage = row["Stage"]
        value = float(row["Normalized_Strength"])

        if edge not in data:
            data[edge] = {}

        data[edge][stage] = value


# ==========================================
# CALCULATE TRANSITIONS
# ==========================================

results = []

for edge, values in data.items():

    for i in range(len(stages) - 1):

        stage1 = stages[i]
        stage2 = stages[i + 1]

        v1 = values.get(stage1, 0)
        v2 = values.get(stage2, 0)

        change = v2 - v1

        results.append({
            "Transition": f"{stage1} -> {stage2}",
            "Concept_A": edge[0],
            "Concept_B": edge[1],
            "Stage_1_Value": round(v1, 6),
            "Stage_2_Value": round(v2, 6),
            "Change": round(change, 6),
            "Absolute_Change": round(abs(change), 6)
        })


# ==========================================
# SORT RESULTS
# ==========================================

results.sort(
    key=lambda x: x["Absolute_Change"],
    reverse=True
)


# ==========================================
# PRINT TOP 15 CHANGES FOR EACH TRANSITION
# ==========================================

print()
print("=" * 75)
print("TRANSITION ANALYSIS")
print("=" * 75)

for i in range(len(stages) - 1):

    transition = f"{stages[i]} -> {stages[i + 1]}"

    transition_rows = [
        row
        for row in results
        if row["Transition"] == transition
    ]

    transition_rows.sort(
        key=lambda x: x["Absolute_Change"],
        reverse=True
    )

    print()
    print("=" * 75)
    print(transition)
    print("=" * 75)

    for row in transition_rows[:15]:

        print(
            f"{row['Concept_A']} -- "
            f"{row['Concept_B']} | "
            f"{row['Stage_1_Value']:.4f} -> "
            f"{row['Stage_2_Value']:.4f} | "
            f"Change: {row['Change']:+.4f}"
        )


# ==========================================
# SAVE CSV
# ==========================================

fieldnames = [
    "Transition",
    "Concept_A",
    "Concept_B",
    "Stage_1_Value",
    "Stage_2_Value",
    "Change",
    "Absolute_Change"
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
    writer.writerows(results)


# ==========================================
# CALCULATE AVERAGE EDGE CHANGE
# ==========================================

transition_scores = {}

for row in results:

    transition = row["Transition"]

    if transition not in transition_scores:
        transition_scores[transition] = []

    transition_scores[transition].append(
        row["Absolute_Change"]
    )


scores = {}

for transition, values in transition_scores.items():

    scores[transition] = sum(values) / len(values)


# ==========================================
# PRINT AVERAGE CHANGE
# ==========================================

print()
print("=" * 75)
print("AVERAGE EDGE CHANGE BY TRANSITION")
print("=" * 75)

for transition, score in sorted(
    scores.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        transition,
        ":",
        round(score, 6)
    )


# ==========================================
# STRONGEST TRANSITION
# ==========================================

strongest = max(
    scores,
    key=scores.get
)

print()
print("=" * 75)
print("STRONGEST EDGE-LEVEL TRANSITION")
print("=" * 75)

print(strongest)

print(
    "Average edge change:",
    round(scores[strongest], 6)
)


# ==========================================
# COMPLETE
# ==========================================

print()
print("=" * 75)
print("ANALYSIS COMPLETE")
print("=" * 75)

print(
    "Relationships analyzed:",
    len(data)
)

print(
    "Created:",
    output_file
)