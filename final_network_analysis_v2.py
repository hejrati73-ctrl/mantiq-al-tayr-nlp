import os
import networkx as nx
from collections import Counter
import pandas as pd

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
    "Ø¬Ø§Ù†", "Ø¯Ù„", "Ø®ÙˆÛŒØ´", "Ø±Ø§Ù‡", "Ø¹Ø´Ù‚", "Ø·Ù„Ø¨", "Ø¯Ø±Ø¯",
    "Ø³ÛŒÙ…Ø±Øº", "Ù…Ø±Øº", "Ù…Ø­Ùˆ", "ÙÙ†Ø§", "Ø¨Ù‚Ø§", "Ø®Ø§Ú©", "ØªÙ†",
    "Ø¬Ø³Ù…", "Ù¾Ø§Ú©", "Ø¹Ù‚Ù„", "Ù†ÙØ³"
}

normalization = {
    "Ø±Ù‡": "Ø±Ø§Ù‡"
}

stage_fa = {
    "opening": "Ø¢ØºØ§Ø²",
    "birds_journey": "Ø³ÙØ± Ù…Ø±ØºØ§Ù†",
    "seven_valleys": "Ù‡ÙØª ÙˆØ§Ø¯ÛŒ",
    "simurgh_encounter": "Ø¯ÛŒØ¯Ø§Ø± Ø³ÛŒÙ…Ø±Øº",
    "final_state": "Ø­Ø§Ù„Øª Ù†Ù‡Ø§ÛŒÛŒ"
}

stage_en = {
    "opening": "Opening",
    "birds_journey": "Birds' Journey",
    "seven_valleys": "Seven Valleys",
    "simurgh_encounter": "Simurgh Encounter",
    "final_state": "Final State"
}

with open("data\\persian_stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(f.read().split())

results_fa = []
results_en = []

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

    # Degree centrality
    degree = nx.degree_centrality(G)

    # Convert co-occurrence strength to path distance
    # Stronger relationship = shorter distance
    for u, v, data in G.edges(data=True):
        data["distance"] = 1.0 / data["weight"]

    # Weighted betweenness centrality
    betweenness = nx.betweenness_centrality(
        G,
        weight="distance"
    )

    # Weighted clustering coefficient
    clustering = nx.clustering(
        G,
        weight="weight"
    )

    # Community detection
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

    stage = filename.split(".txt_")[0]

    for concept in G.nodes():

        degree_score = degree.get(concept, 0)
        betweenness_score = betweenness.get(concept, 0)
        clustering_score = clustering.get(concept, 0)

        result_fa = {
            "Ù…Ø±Ø­Ù„Ù‡": stage_fa.get(stage, stage),
            "Ù…ÙÙ‡ÙˆÙ…": concept,
            "ÙØ±Ø§ÙˆØ§Ù†ÛŒ": frequency[concept],
            "Ù…Ø±Ú©Ø²ÛŒÙ‘Øª Ø¯Ø±Ø¬Ù‡â€ŒØ§ÛŒ": round(degree_score, 4),
            "Ù…Ø±Ú©Ø²ÛŒÙ‘Øª Ø¨ÛŒÙ†Ø§Ø¨ÛŒÙ†ÛŒ": round(betweenness_score, 4),
            "Ø¶Ø±ÛŒØ¨ Ø®ÙˆØ´Ù‡â€ŒØ¨Ù†Ø¯ÛŒ": round(clustering_score, 4),
            "ØªØ¹Ø¯Ø§Ø¯ Ú¯Ø±Ù‡â€ŒÙ‡Ø§": G.number_of_nodes(),
            "ØªØ¹Ø¯Ø§Ø¯ ÛŒØ§Ù„â€ŒÙ‡Ø§": G.number_of_edges(),
            "Ú†Ú¯Ø§Ù„ÛŒ Ø´Ø¨Ú©Ù‡": round(nx.density(G), 4),
            "Ù…ÛŒØ§Ù†Ú¯ÛŒÙ† Ø¯Ø±Ø¬Ù‡": round(
                sum(dict(G.degree()).values())
                / G.number_of_nodes(),
                4
            ),
            "Ø§Ø¬Ø²Ø§ÛŒ Ù‡Ù…Ø¨Ù†Ø¯": nx.number_connected_components(G),
            "ØªØ¹Ø¯Ø§Ø¯ Ø§Ø¬ØªÙ…Ø§Ø¹Ø§Øª": len(communities),
            "Ù…Ø¯ÙˆÙ„Ø§Ø±ÛŒØªÛŒ": round(modularity, 4)
        }

        result_en = {
            "Stage": stage_en.get(stage, stage),
            "Concept": concept,
            "Frequency": frequency[concept],
            "Degree Centrality": round(degree_score, 4),
            "Betweenness Centrality": round(betweenness_score, 4),
            "Clustering Coefficient": round(clustering_score, 4),
            "Nodes": G.number_of_nodes(),
            "Edges": G.number_of_edges(),
            "Network Density": round(nx.density(G), 4),
            "Average Degree": round(
                sum(dict(G.degree()).values())
                / G.number_of_nodes(),
                4
            ),
            "Connected Components": nx.number_connected_components(G),
            "Communities": len(communities),
            "Modularity": round(modularity, 4)
        }

        results_fa.append(result_fa)
        results_en.append(result_en)

df_fa = pd.DataFrame(results_fa)
df_en = pd.DataFrame(results_en)

if not df_fa.empty:

    df_fa = df_fa.sort_values(
        ["Ù…Ø±Ø­Ù„Ù‡", "Ù…Ø±Ú©Ø²ÛŒÙ‘Øª Ø¯Ø±Ø¬Ù‡â€ŒØ§ÛŒ"],
        ascending=[True, False]
    )

    df_en = df_en.sort_values(
        ["Stage", "Degree Centrality"],
        ascending=[True, False]
    )

df_fa.to_csv(
    "final_network_analysis_v2_fa.csv",
    index=False,
    encoding="utf-8-sig"
)

df_en.to_csv(
    "final_network_analysis_v2_en.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print("=" * 70)
print("FINAL NETWORK ANALYSIS - V2")
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
print("final_network_analysis_v2_fa.csv")
print("final_network_analysis_v2_en.csv")

print()
print("Analysis complete.")

