import os
import networkx as nx
from collections import Counter
import pandas as pd

# ============================================================
# FINAL NETWORK ANALYSIS
# Persian + English outputs
# ============================================================

input_folder = "sections"

files = [
    "opening.txt_01",
    "birds_journey.txt_02",
    "seven_valleys.txt_03",
    "simurgh_encounter.txt_04",
    "final_state.txt_05"
]

window_size = 5
min_frequency = 15

keywords = {
    "جان", "دل", "خویش", "راه", "عشق", "طلب", "درد",
    "سیمرغ", "مرغ", "محو", "فنا", "بقا", "خاک", "تن",
    "جسم", "پاک", "عقل", "نفس"
}

normalization = {
    "ره": "راه"
}

# ------------------------------------------------------------
# Stage labels
# ------------------------------------------------------------

stage_fa = {
    "opening": "آغاز",
    "birds_journey": "سفر مرغان",
    "seven_valleys": "هفت وادی",
    "simurgh_encounter": "دیدار سیمرغ",
    "final_state": "حالت نهایی"
}

stage_en = {
    "opening": "Opening",
    "birds_journey": "Birds' Journey",
    "seven_valleys": "Seven Valleys",
    "simurgh_encounter": "Simurgh Encounter",
    "final_state": "Final State"
}

# ------------------------------------------------------------
# Read stopwords
# ------------------------------------------------------------

with open("persian_stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(f.read().split())

# ------------------------------------------------------------
# Results
# ------------------------------------------------------------

results_fa = []
results_en = []

# ------------------------------------------------------------
# Main analysis
# ------------------------------------------------------------

for filename in files:

    filepath = os.path.join(input_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = []

    for w in text.split():

        if w in normalization:
            w = normalization[w]

        if w not in stopwords and w in keywords:
            words.append(w)

    frequency = Counter(words)

    # --------------------------------------------------------
    # Build co-occurrence pairs
    # --------------------------------------------------------

    pairs = Counter()

    for i in range(len(words)):

        window = words[i:i + window_size]

        for a in range(len(window)):
            for b in range(a + 1, len(window)):

                w1 = window[a]
                w2 = window[b]

                if w1 != w2:

                    pair = tuple(sorted((w1, w2)))
                    pairs[pair] += 1

    # --------------------------------------------------------
    # Build network
    # --------------------------------------------------------

    G = nx.Graph()

    for (w1, w2), count in pairs.items():

        if count >= min_frequency:

            G.add_edge(
                w1,
                w2,
                weight=count
            )

    if G.number_of_nodes() == 0:
        continue

    # --------------------------------------------------------
    # Network metrics
    # --------------------------------------------------------

    degree = nx.degree_centrality(G)

    betweenness = nx.betweenness_centrality(
        G,
        weight="weight"
    )

    clustering = nx.clustering(
        G,
        weight="weight"
    )

    # --------------------------------------------------------
    # Communities
    # --------------------------------------------------------

    communities = list(
        nx.community.greedy_modularity_communities(
            G,
            weight="weight"
        )
    )

    modularity = nx.community.modularity(
        G,
        communities,
        weight="weight"
    )

    # --------------------------------------------------------
    # Stage name
    # --------------------------------------------------------

    stage = filename.split(".txt_")[0]

    # --------------------------------------------------------
    # Save EVERY concept appearing in the network
    # --------------------------------------------------------

    for concept in G.nodes():

        degree_score = degree.get(concept, 0)
        betweenness_score = betweenness.get(concept, 0)
        clustering_score = clustering.get(concept, 0)

        result_fa = {

            "مرحله": stage_fa.get(stage, stage),

            "مفهوم": concept,

            "فراوانی": frequency[concept],

            "مرکزیّت درجه‌ای":
                round(degree_score, 4),

            "مرکزیّت بینابینی":
                round(betweenness_score, 4),

            "ضریب خوشه‌بندی":
                round(clustering_score, 4),

            "تعداد گره‌ها":
                G.number_of_nodes(),

            "تعداد یال‌ها":
                G.number_of_edges(),

            "چگالی شبکه":
                round(nx.density(G), 4),

            "میانگین درجه":
                round(
                    sum(dict(G.degree()).values())
                    / G.number_of_nodes(),
                    4
                ),

            "اجزای همبند":
                nx.number_connected_components(G),

            "تعداد اجتماعات":
                len(communities),

            "مدولاریتی":
                round(modularity, 4)
        }

        result_en = {

            "Stage":
                stage_en.get(stage, stage),

            "Concept":
                concept,

            "Frequency":
                frequency[concept],

            "Degree Centrality":
                round(degree_score, 4),

            "Betweenness Centrality":
                round(betweenness_score, 4),

            "Clustering Coefficient":
                round(clustering_score, 4),

            "Nodes":
                G.number_of_nodes(),

            "Edges":
                G.number_of_edges(),

            "Network Density":
                round(nx.density(G), 4),

            "Average Degree":
                round(
                    sum(dict(G.degree()).values())
                    / G.number_of_nodes(),
                    4
                ),

            "Connected Components":
                nx.number_connected_components(G),

            "Communities":
                len(communities),

            "Modularity":
                round(modularity, 4)
        }

        results_fa.append(result_fa)
        results_en.append(result_en)

# ------------------------------------------------------------
# Create DataFrames
# ------------------------------------------------------------

df_fa = pd.DataFrame(results_fa)
df_en = pd.DataFrame(results_en)

# ------------------------------------------------------------
# Sort results
# ------------------------------------------------------------

if not df_fa.empty:

    df_fa = df_fa.sort_values(
        ["مرحله", "مرکزیّت درجه‌ای"],
        ascending=[True, False]
    )

    df_en = df_en.sort_values(
        ["Stage", "Degree Centrality"],
        ascending=[True, False]
    )

# ------------------------------------------------------------
# Export Persian
# ------------------------------------------------------------

df_fa.to_csv(
    "final_network_analysis_fa.csv",
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# Export English
# ------------------------------------------------------------

df_en.to_csv(
    "final_network_analysis_en.csv",
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# Console summary
# ------------------------------------------------------------

print()
print("=" * 70)
print("FINAL NETWORK ANALYSIS")
print("=" * 70)

print()

for stage in stage_en.values():

    subset = df_en[df_en["Stage"] == stage]

    print(
        stage,
        "| Concepts:", len(subset)
    )

print()
print("Total rows:", len(df_en))
print()
print("Created:")
print("final_network_analysis_fa.csv")
print("final_network_analysis_en.csv")
print()
print("Analysis complete.")