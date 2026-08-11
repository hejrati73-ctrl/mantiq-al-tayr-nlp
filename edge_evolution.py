import os
import csv
import networkx as nx
from collections import Counter


# ============================================================
# SETTINGS
# ============================================================

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

CONCEPTS = [
    "جان",
    "دل",
    "خویش",
    "راه",
    "عشق",
    "طلب",
    "درد",
    "سیمرغ",
    "مرغ",
    "محو",
    "فنا",
    "بقا",
    "خاک",
    "تن",
    "جسم",
    "پاک",
    "عقل",
    "نفس"
]

KEYWORDS = set(CONCEPTS)

NORMALIZATION = {
    "ره": "راه"
}


# ============================================================
# LOAD STOPWORDS
# ============================================================

with open(
    "persian_stopwords.txt",
    "r",
    encoding="utf-8"
) as f:
    stopwords = set(f.read().split())


# ============================================================
# BUILD CO-OCCURRENCE NETWORK
# ============================================================

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
            and word in KEYWORDS
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


# ============================================================
# EXTRACT EDGE DATA FOR EACH STAGE
# ============================================================

edge_data = {}

for stage, filename in zip(
    STAGES,
    FILES
):

    G = build_network(filename)

    edge_data[stage] = {}

    for u, v, data in G.edges(data=True):

        pair = tuple(
            sorted((u, v))
        )

        edge_data[stage][pair] = data["weight"]


# ============================================================
# ALL EDGES ACROSS ALL STAGES
# ============================================================

all_edges = set()

for stage in STAGES:

    all_edges.update(
        edge_data[stage].keys()
    )


# ============================================================
# CREATE EDGE EVOLUTION TABLE
# ============================================================

rows = []

for edge in sorted(all_edges):

    values = [
        edge_data[stage].get(
            edge,
            0
        )
        for stage in STAGES
    ]

    presence = [
        value > 0
        for value in values
    ]

    pattern = "".join(
        "1" if present else "0"
        for present in presence
    )

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    if pattern == "11111":

        classification = "Persistent"

    elif pattern == "00001":

        classification = "Late-emerging"

    elif pattern == "10000":

        classification = "Disappearing"

    elif pattern == "10001":

        classification = "Re-emerging"

    elif sum(presence) <= 2:

        classification = "Transient"

    else:

        classification = "Variable"

    rows.append({
        "Concept_A": edge[0],
        "Concept_B": edge[1],
        "Opening": values[0],
        "Birds_Journey": values[1],
        "Seven_Valleys": values[2],
        "Simurgh_Encounter": values[3],
        "Final_State": values[4],
        "Presence_Pattern": pattern,
        "Classification": classification
    })


# ============================================================
# CALCULATE TOTAL EDGE STRENGTH
# ============================================================

for row in rows:

    row["Total"] = (
        row["Opening"]
        + row["Birds_Journey"]
        + row["Seven_Valleys"]
        + row["Simurgh_Encounter"]
        + row["Final_State"]
    )


# ============================================================
# SORT BY TOTAL EDGE STRENGTH
# ============================================================

rows.sort(
    key=lambda row: row["Total"],
    reverse=True
)


# ============================================================
# PRINT ANALYSIS
# ============================================================

print("=" * 80)
print("EDGE EVOLUTION ANALYSIS")
print("=" * 80)

print()
print("Window size:", WINDOW_SIZE)
print("Minimum frequency:", MIN_FREQUENCY)
print("Number of stages:", len(STAGES))
print("Total relationships:", len(rows))

print()
print("Top 30 conceptual relationships:")
print()

for row in rows[:30]:

    print(
        f"{row['Concept_A']} -- {row['Concept_B']} : "
        f"{row['Opening']} | "
        f"{row['Birds_Journey']} | "
        f"{row['Seven_Valleys']} | "
        f"{row['Simurgh_Encounter']} | "
        f"{row['Final_State']} "
        f"[{row['Classification']}]"
    )


# ============================================================
# EDGE CLASSIFICATION SUMMARY
# ============================================================

print()
print("=" * 80)
print("EDGE CLASSIFICATION SUMMARY")
print("=" * 80)

categories = {}

for row in rows:

    category = row["Classification"]

    if category not in categories:

        categories[category] = []

    categories[category].append(
        f"{row['Concept_A']}--{row['Concept_B']}"
    )


for category in [
    "Persistent",
    "Re-emerging",
    "Late-emerging",
    "Disappearing",
    "Variable",
    "Transient"
]:

    if category not in categories:
        continue

    edges = categories[category]

    print()
    print(
        f"{category} ({len(edges)} relationships):"
    )

    print(
        " | ".join(edges[:30])
    )


# ============================================================
# SAVE CSV
# ============================================================

output_file = "edge_evolution.csv"

fieldnames = [
    "Concept_A",
    "Concept_B",
    "Opening",
    "Birds_Journey",
    "Seven_Valleys",
    "Simurgh_Encounter",
    "Final_State",
    "Presence_Pattern",
    "Classification",
    "Total"
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

    writer.writerows(rows)


# ============================================================
# FINAL MESSAGE
# ============================================================

print()
print("CSV created:")
print(output_file)

print()
print("Total relationships:", len(rows))

print()
print("Analysis completed successfully.")