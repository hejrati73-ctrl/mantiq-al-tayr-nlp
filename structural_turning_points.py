import csv

# ==================================================
# INPUT
# ==================================================

input_file = "final_results_table.csv"

stages = [
    "opening",
    "birds_journey",
    "seven_valleys",
    "simurgh_encounter",
    "final_state"
]

# ==================================================
# READ DATA
# ==================================================

data = {}

with open(
    input_file,
    "r",
    encoding="utf-8-sig"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        stage = row["Stage"]

        data[stage] = {
            "Density": float(row["Density"]),
            "Average Degree": float(
                row["Average Degree"]
            ),
            "Average Clustering": float(
                row["Average Clustering"]
            ),
            "Number of Communities": int(
                row["Number of Communities"]
            ),
            "Modularity": float(
                row["Modularity"]
            )
        }


# ==================================================
# CALCULATE CHANGES
# ==================================================

transitions = []

metrics = [
    "Density",
    "Average Degree",
    "Average Clustering",
    "Number of Communities",
    "Modularity"
]

for i in range(len(stages) - 1):

    stage_a = stages[i]
    stage_b = stages[i + 1]

    row = {
        "From": stage_a,
        "To": stage_b
    }

    total_change = 0

    for metric in metrics:

        old = data[stage_a][metric]
        new = data[stage_b][metric]

        absolute_change = new - old

        if old != 0:
            percent_change = (
                absolute_change / old
            ) * 100
        else:
            percent_change = 0

        row[
            metric + " Change"
        ] = round(
            absolute_change,
            4
        )

        row[
            metric + " % Change"
        ] = round(
            percent_change,
            2
        )

        # Standardized magnitude
        if old != 0:
            normalized_change = abs(
                absolute_change / old
            )
        else:
            normalized_change = abs(
                absolute_change
            )

        total_change += normalized_change

    row[
        "Structural Change Score"
    ] = round(
        total_change / len(metrics),
        4
    )

    transitions.append(row)


# ==================================================
# RANK TRANSITIONS
# ==================================================

transitions.sort(
    key=lambda x:
        x["Structural Change Score"],
    reverse=True
)


# ==================================================
# PRINT RESULTS
# ==================================================

print()
print("=" * 75)
print("STRUCTURAL TURNING POINT ANALYSIS")
print("=" * 75)

for rank, row in enumerate(
    transitions,
    start=1
):

    print()
    print(
        f"{rank}. "
        f"{row['From']} -> {row['To']}"
    )

    print(
        "Structural Change Score:",
        row["Structural Change Score"]
    )

    for metric in metrics:

        print(
            f"{metric}: "
            f"{row[metric + ' Change']} "
            f"("
            f"{row[metric + ' % Change']}%"
            f")"
        )


# ==================================================
# MOST IMPORTANT TURNING POINT
# ==================================================

strongest = transitions[0]

print()
print("=" * 75)
print("STRONGEST STRUCTURAL TURNING POINT")
print("=" * 75)

print(
    strongest["From"],
    "->",
    strongest["To"]
)

print(
    "Score:",
    strongest["Structural Change Score"]
)


# ==================================================
# SAVE CSV
# ==================================================

fieldnames = [
    "From",
    "To"
]

for metric in metrics:

    fieldnames.append(
        metric + " Change"
    )

    fieldnames.append(
        metric + " % Change"
    )

fieldnames.append(
    "Structural Change Score"
)


with open(
    "structural_turning_points.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(
        transitions
    )


print()
print("=" * 75)
print("ANALYSIS COMPLETE")
print("=" * 75)

print(
    "Created:",
    "structural_turning_points.csv"
)