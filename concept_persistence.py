import os
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
    "Birds' Journey",
    "Seven Valleys",
    "Simurgh Encounter",
    "Final State"
]

WINDOW_SIZE = 5
MIN_FREQUENCY = 15

CONCEPTS = [
    "جان", "دل", "خویش", "راه", "عشق", "طلب", "درد",
    "سیمرغ", "مرغ", "محو", "فنا", "بقا", "خاک", "تن",
    "جسم", "پاک", "عقل", "نفس"
]

KEYWORDS = set(CONCEPTS)

# ==================================================
# NORMALIZATION
# ==================================================

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


# ==================================================
# BUILD PRESENCE / CENTRALITY MATRIX
# ==================================================

degree_by_stage = {}

for filename in FILES:

    G = build_network(filename)

    degree = nx.degree_centrality(G)

    degree_by_stage[filename] = degree


# ==================================================
# CLASSIFY CONCEPTS
# ==================================================

print("=" * 75)
print("CONCEPT PERSISTENCE / EMERGENCE ANALYSIS")
print("=" * 75)

results = []

for concept in CONCEPTS:

    values = []

    for filename in FILES:

        value = degree_by_stage[
            filename
        ].get(concept, 0)

        values.append(value)

    # ----------------------------------------------
    # Presence
    # ----------------------------------------------

    presence = [
        value > 0
        for value in values
    ]

    first_stage = None
    last_stage = None

    for i, present in enumerate(presence):

        if present:

            if first_stage is None:
                first_stage = i

            last_stage = i

    # ----------------------------------------------
    # Classification
    # ----------------------------------------------

    if not any(presence):

        classification = "Absent"

    elif all(presence):

        classification = "Persistent"

    elif presence[0] is False and all(
        presence[i]
        for i in range(1, len(presence))
    ):

        classification = "Emerging"

    elif (
        presence[0]
        and not presence[-1]
        and all(
            not presence[i]
            for i in range(1, len(presence))
        )
    ):

        classification = "Disappearing"

    elif (
        presence[0]
        and presence[-1]
        and not all(presence)
    ):

        classification = "Re-emerging"

    elif (
        not presence[0]
        and presence[-1]
    ):

        classification = "Late-emerging"

    else:

        classification = "Transient"

    # ----------------------------------------------
    # Store
    # ----------------------------------------------

    results.append({
        "concept": concept,
        "values": values,
        "classification": classification
    })


# ==================================================
# PRINT RESULTS
# ==================================================

for result in results:

    print("\n" + result["concept"])

    print(
        "Centrality:",
        " | ".join(
            str(round(v, 4))
            for v in result["values"]
        )
    )

    print(
        "Classification:",
        result["classification"]
    )


# ==================================================
# SUMMARY
# ==================================================

print("\n")
print("=" * 75)
print("SUMMARY")
print("=" * 75)

categories = {}

for result in results:

    category = result["classification"]

    if category not in categories:

        categories[category] = []

    categories[category].append(
        result["concept"]
    )


for category, concepts in categories.items():

    print(
        f"\n{category}:"
    )

    print(
        " | ".join(concepts)
    )


# ==================================================
# SAVE CSV
# ==================================================

import csv

output_file = "concept_persistence.csv"

with open(
    output_file,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "Concept",
        "Opening",
        "Birds_Journey",
        "Seven_Valleys",
        "Simurgh_Encounter",
        "Final_State",
        "Classification"
    ])

    for result in results:

        writer.writerow([
            result["concept"],
            round(result["values"][0], 4),
            round(result["values"][1], 4),
            round(result["values"][2], 4),
            round(result["values"][3], 4),
            round(result["values"][4], 4),
            result["classification"]
        ])


print("\n")
print("CSV created:")
print(output_file)