import os
import csv
import networkx as nx
from collections import Counter

# ==================================================
# SETTINGS
# ==================================================

INPUT_FOLDER = "sections"

FILES = [
    "opening.txt_01",
    "birds_journey.txt_02",
    "seven_valleys.txt_03",
    "simurgh_encounter.txt_04",
    "final_state.txt_05"
]

STAGES = [
    "Opening",
    "Birds_Journey",
    "Seven_Valleys",
    "Simurgh_Encounter",
    "Final_State"
]

WINDOW_SIZE = 5
MIN_FREQUENCY = 15

CONCEPTS = {
    "جان", "دل", "خویش", "راه", "ره", "عشق", "طلب", "درد",
    "سیمرغ", "مرغ", "محو", "فنا", "بقا", "خاک", "تن",
    "جسم", "پاک", "عقل", "نفس"
}

NORMALIZATION = {
    "ره": "راه"
}


# ==================================================
# STOPWORDS
# ==================================================

with open(
    "persian_stopwords.txt",
    "r",
    encoding="utf-8"
) as f:

    stopwords = set(f.read().split())


# ==================================================
# BUILD NETWORK
# ==================================================

def build_network(filename):

    filepath = os.path.join(
        INPUT_FOLDER,
        filename
    )

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    words = []

    for word in text.split():

        if word in NORMALIZATION:
            word = NORMALIZATION[word]

        if (
            word not in stopwords
            and word in CONCEPTS
        ):
            words.append(word)

    pairs = Counter()

    for i in range(len(words)):

        window = words[
            i:i + WINDOW_SIZE
        ]

        for a in range(len(window)):

            for b in range(
                a + 1,
                len(window)
            ):

                w1 = window[a]
                w2 = window[b]

                if w1 != w2:

                    pair = tuple(
                        sorted((w1, w2))
                    )

                    pairs[pair] += 1

    G = nx.Graph()

    for (w1, w2), count in pairs.items():

        if count >= MIN_FREQUENCY:

            G.add_edge(
                w1,
                w2,
                weight=count
            )

    return G


# ==================================================
# BUILD ALL NETWORKS
# ==================================================

networks = {}

for stage, filename in zip(
    STAGES,
    FILES
):

    networks[stage] = build_network(
        filename
    )


# ==================================================
# NORMALIZED EDGE STRENGTH
# ==================================================

edge_rows = []

for stage in STAGES:

    G = networks[stage]

    total_weight = sum(
        data["weight"]
        for _, _, data
        in G.edges(data=True)
    )

    print("\n" + "=" * 70)
    print(stage)
    print("=" * 70)

    print(
        "Total edge weight:",
        total_weight
    )

    if total_weight == 0:
        continue

    for u, v, data in G.edges(
        data=True
    ):

        weight = data["weight"]

        normalized = (
            weight / total_weight
        )

        edge_rows.append({
            "Stage": stage,
            "Concept_A": u,
            "Concept_B": v,
            "Raw_Weight": weight,
            "Total_Edge_Weight": total_weight,
            "Normalized_Strength": round(
                normalized,
                6
            )
        })


# ==================================================
# CONVERT TO EDGE-BY-STAGE TABLE
# ==================================================

all_edges = set()

for row in edge_rows:

    all_edges.add(
        tuple(sorted([
            row["Concept_A"],
            row["Concept_B"]
        ]))
    )


normalized_data = {}

for row in edge_rows:

    edge = tuple(sorted([
        row["Concept_A"],
        row["Concept_B"]
    ]))

    stage = row["Stage"]

    if edge not in normalized_data:
        normalized_data[edge] = {}

    normalized_data[edge][stage] = {
        "raw": row["Raw_Weight"],
        "normalized": row[
            "Normalized_Strength"
        ]
    }


# ==================================================
# CREATE COMPARISON TABLE
# ==================================================

comparison_rows = []

for edge in sorted(all_edges):

    row = {
        "Concept_A": edge[0],
        "Concept_B": edge[1]
    }

    normalized_values = []

    raw_values = []

    for stage in STAGES:

        data = normalized_data.get(
            edge,
            {}
        ).get(
            stage
        )

        if data:

            raw = data["raw"]
            normalized = data[
                "normalized"
            ]

        else:

            raw = 0
            normalized = 0

        row[
            stage + "_Raw"
        ] = raw

        row[
            stage + "_Normalized"
        ] = normalized

        normalized_values.append(
            normalized
        )

        raw_values.append(
            raw
        )

    row["Mean_Normalized"] = round(
        sum(normalized_values) /
        len(normalized_values),
        6
    )

    row["Max_Normalized"] = round(
        max(normalized_values),
        6
    )

    row["Min_Normalized"] = round(
        min(normalized_values),
        6
    )

    row["Range"] = round(
        max(normalized_values) -
        min(normalized_values),
        6
    )

    comparison_rows.append(row)


# ==================================================
# SORT BY MEAN NORMALIZED STRENGTH
# ==================================================

comparison_rows.sort(
    key=lambda x:
        x["Mean_Normalized"],
    reverse=True
)


# ==================================================
# PRINT TOP RELATIONSHIPS
# ==================================================

print("\n")
print("=" * 70)
print("TOP NORMALIZED RELATIONSHIPS")
print("=" * 70)

for row in comparison_rows[:30]:

    print(
        f"{row['Concept_A']} -- "
        f"{row['Concept_B']} : "
        f"{row['Opening_Normalized']} | "
        f"{row['Birds_Journey_Normalized']} | "
        f"{row['Seven_Valleys_Normalized']} | "
        f"{row['Simurgh_Encounter_Normalized']} | "
        f"{row['Final_State_Normalized']} "
        f"| Mean = "
        f"{row['Mean_Normalized']}"
    )


# ==================================================
# STRONGEST RELATIONSHIP PER STAGE
# ==================================================

print("\n")
print("=" * 70)
print("STRONGEST NORMALIZED RELATIONSHIP BY STAGE")
print("=" * 70)

for stage in STAGES:

    stage_rows = [
        row
        for row in edge_rows
        if row["Stage"] == stage
    ]

    stage_rows.sort(
        key=lambda x:
            x["Normalized_Strength"],
        reverse=True
    )

    print("\n" + stage)

    for row in stage_rows[:10]:

        print(
            f"{row['Concept_A']} -- "
            f"{row['Concept_B']} : "
            f"raw={row['Raw_Weight']} "
            f"normalized="
            f"{row['Normalized_Strength']}"
        )


# ==================================================
# SAVE STAGE-LEVEL DATA
# ==================================================

with open(
    "normalized_edge_evolution_long.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Stage",
            "Concept_A",
            "Concept_B",
            "Raw_Weight",
            "Total_Edge_Weight",
            "Normalized_Strength"
        ]
    )

    writer.writeheader()

    writer.writerows(edge_rows)


# ==================================================
# SAVE COMPARISON TABLE
# ==================================================

fieldnames = [
    "Concept_A",
    "Concept_B"
]

for stage in STAGES:

    fieldnames.extend([
        stage + "_Raw",
        stage + "_Normalized"
    ])

fieldnames.extend([
    "Mean_Normalized",
    "Max_Normalized",
    "Min_Normalized",
    "Range"
])


with open(
    "normalized_edge_evolution.csv",
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
        comparison_rows
    )


# ==================================================
# DONE
# ==================================================

print("\n")
print("=" * 70)
print("NORMALIZED EDGE ANALYSIS COMPLETE")
print("=" * 70)

print(
    "Relationships:",
    len(comparison_rows)
)

print(
    "Created:",
    "normalized_edge_evolution_long.csv"
)

print(
    "Created:",
    "normalized_edge_evolution.csv"
)