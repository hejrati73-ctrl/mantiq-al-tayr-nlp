import os
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# ==================================================
# SETTINGS
# ==================================================

INPUT_FOLDER = "sections"

OUTPUT_FA = "concept_evolution_fa.png"
OUTPUT_EN = "concept_evolution_en.png"

WINDOW_SIZE = 5
MIN_FREQUENCY = 15

FILES = [
    "opening.txt_01",
    "birds_journey.txt_02",
    "seven_valleys.txt_03",
    "simurgh_encounter.txt_04",
    "final_state.txt_05"
]

STAGES_EN = [
    "Opening",
    "Birds' Journey",
    "Seven Valleys",
    "Simurgh Encounter",
    "Final State"
]

STAGES_FA = [
    "آغاز",
    "سفر پرندگان",
    "هفت وادی",
    "دیدار سیمرغ",
    "وضعیت نهایی"
]

# ==================================================
# KEY CONCEPTS
# ==================================================

CONCEPTS = [
    "جان",
    "دل",
    "راه",
    "خویش",
    "عشق",
    "درد",
    "عقل",
    "نفس",
    "خاک",
    "پاک",
    "طلب",
    "محو",
    "فنا",
    "بقا",
    "سیمرغ",
    "مرغ",
    "تن",
    "جسم"
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

    for (
        (w1, w2),
        count
    ) in pairs.items():

        if count >= MIN_FREQUENCY:

            G.add_edge(
                w1,
                w2,
                weight=count
            )

    return G

# ==================================================
# CALCULATE DEGREE CENTRALITY
# ==================================================

degree_by_stage = {}

for filename in FILES:

    G = build_network(filename)

    degree = nx.degree_centrality(G)

    degree_by_stage[filename] = degree

# ==================================================
# PRINT DATA
# ==================================================

print("=" * 70)
print("CONCEPT EVOLUTION")
print("=" * 70)

for concept in CONCEPTS:

    values = []

    for filename in FILES:

        score = degree_by_stage[
            filename
        ].get(concept, 0)

        values.append(score)

    print(
        concept,
        " | ".join(
            str(round(v, 4))
            for v in values
        )
    )

# ==================================================
# SELECT MOST IMPORTANT CONCEPTS
# ==================================================

# Calculate mean centrality across stages

concept_mean = {}

for concept in CONCEPTS:

    values = [
        degree_by_stage[file].get(
            concept,
            0
        )
        for file in FILES
    ]

    concept_mean[concept] = (
        sum(values) / len(values)
    )

# Select top 8 concepts

TOP_CONCEPTS = sorted(
    concept_mean,
    key=concept_mean.get,
    reverse=True
)[:8]

print("\nTop concepts selected:")
print(", ".join(TOP_CONCEPTS))

# ==================================================
# FUNCTION FOR PLOTTING
# ==================================================

def create_plot(
    stages,
    output_file,
    title,
    xlabel,
    ylabel
):

    plt.figure(
        figsize=(12, 7)
    )

    for concept in TOP_CONCEPTS:

        values = [
            degree_by_stage[file].get(
                concept,
                0
            )
            for file in FILES
        ]

        plt.plot(
            stages,
            values,
            marker="o",
            linewidth=2,
            label=concept
        )

    plt.title(
        title,
        fontsize=18
    )

    plt.xlabel(
        xlabel,
        fontsize=13
    )

    plt.ylabel(
        ylabel,
        fontsize=13
    )

    plt.xticks(
        rotation=25
    )

    plt.legend(
        fontsize=10,
        ncol=2
    )

    plt.grid(
        alpha=0.25
    )

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

# ==================================================
# ENGLISH FIGURE
# ==================================================

create_plot(
    STAGES_EN,
    OUTPUT_EN,
    "Evolution of Conceptual Centrality Across Narrative Stages",
    "Narrative Stage",
    "Degree Centrality"
)

# ==================================================
# PERSIAN FIGURE
# ==================================================

create_plot(
    STAGES_FA,
    OUTPUT_FA,
    "تحول مرکزیت مفاهیم در مراحل روایی منطق‌الطیر",
    "مرحله روایی",
    "مرکزیت درجه‌ای"
)

print("\nFigures created:")
print(OUTPUT_FA)
print(OUTPUT_EN)