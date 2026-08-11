import csv

# ============================================================
# FILES
# ============================================================

input_file = "normalized_edge_evolution_long.csv"

output_en = "edge_status_analysis_en.csv"
output_fa = "edge_status_analysis_fa.csv"

stages = [
    "Opening",
    "Birds_Journey",
    "Seven_Valleys",
    "Simurgh_Encounter",
    "Final_State"
]

# ============================================================
# READ DATA
# ============================================================

data = {}

with open(input_file, "r", encoding="utf-8-sig") as f:

    reader = csv.DictReader(f)

    for row in reader:

        edge = tuple(sorted([
            row["Concept_A"],
            row["Concept_B"]
        ]))

        stage = row["Stage"]

        strength = float(row["Normalized_Strength"])

        if edge not in data:
            data[edge] = {}

        data[edge][stage] = strength


# ============================================================
# CREATE ALL EDGE × STAGE RECORDS
# ============================================================

results = []

for edge in sorted(data.keys()):

    previous_strength = 0.0

    for stage in stages:

        current_strength = data[edge].get(stage, 0.0)

        change = current_strength - previous_strength

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if stage == "Opening":

            if current_strength > 0:
                status_en = "Emerging"
                status_fa = "ظهوریافته"
            else:
                status_en = "Stable"
                status_fa = "پایدار"

        else:

            if previous_strength == 0 and current_strength > 0:
                status_en = "Emerging"
                status_fa = "ظهوریافته"

            elif previous_strength > 0 and current_strength == 0:
                status_en = "Weakening"
                status_fa = "تضعیف‌شده"

            elif change > 0:
                status_en = "Strengthening"
                status_fa = "تقویت‌شونده"

            elif change < 0:
                status_en = "Weakening"
                status_fa = "تضعیف‌شده"

            else:
                status_en = "Stable"
                status_fa = "پایدار"

        results.append({
            "Stage": stage,
            "Concept_A": edge[0],
            "Concept_B": edge[1],
            "Normalized_Strength": round(current_strength, 6),
            "Previous_Strength": round(previous_strength, 6),
            "Change": round(change, 6),
            "Status_EN": status_en,
            "Status_FA": status_fa
        })

        previous_strength = current_strength


# ============================================================
# ENGLISH OUTPUT
# ============================================================

fields_en = [
    "Stage",
    "Concept_A",
    "Concept_B",
    "Normalized_Strength",
    "Previous_Strength",
    "Change",
    "Status"
]

with open(
    output_en,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fields_en
    )

    writer.writeheader()

    for row in results:

        writer.writerow({
            "Stage": row["Stage"],
            "Concept_A": row["Concept_A"],
            "Concept_B": row["Concept_B"],
            "Normalized_Strength":
                row["Normalized_Strength"],
            "Previous_Strength":
                row["Previous_Strength"],
            "Change":
                row["Change"],
            "Status":
                row["Status_EN"]
        })


# ============================================================
# PERSIAN OUTPUT
# ============================================================

fields_fa = [
    "مرحله",
    "مفهوم_الف",
    "مفهوم_ب",
    "قدرت_نرمال‌شده",
    "قدرت_مرحله_قبل",
    "تغییر",
    "وضعیت"
]

with open(
    output_fa,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fields_fa
    )

    writer.writeheader()

    for row in results:

        writer.writerow({
            "مرحله": row["Stage"],
            "مفهوم_الف": row["Concept_A"],
            "مفهوم_ب": row["Concept_B"],
            "قدرت_نرمال‌شده":
                row["Normalized_Strength"],
            "قدرت_مرحله_قبل":
                row["Previous_Strength"],
            "تغییر":
                row["Change"],
            "وضعیت":
                row["Status_FA"]
        })


# ============================================================
# SUMMARY
# ============================================================

status_counts = {
    "Emerging": 0,
    "Strengthening": 0,
    "Weakening": 0,
    "Stable": 0
}

for row in results:
    status_counts[row["Status_EN"]] += 1


print()
print("=" * 70)
print("EDGE STATUS ANALYSIS")
print("=" * 70)

print()
print("Unique relationships:", len(data))
print("Total status records:", len(results))

print()
print("Status counts:")

for status, count in status_counts.items():
    print(f"{status}: {count}")

print()
print("Created:")
print(output_en)
print(output_fa)

print()
print("=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)