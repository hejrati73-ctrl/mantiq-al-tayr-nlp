import os
import networkx as nx
from collections import Counter

input_folder = "sections"

files = [
    "opening.txt_01",
    "birds_journey.txt_02",
    "seven_valleys.txt_03",
    "simurgh_encounter.txt_04",
    "final_state.txt_05"
]

window_sizes = [3, 5, 7]
thresholds = [10, 15, 20]

keywords = {
    "جان", "دل", "خویش", "راه", "ره", "عشق",
    "طلب", "درد", "سیمرغ", "مرغ", "محو", "فنا",
    "بقا", "خاک", "تن", "جسم", "پاک", "عقل", "نفس"
}

with open("persian_stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(f.read().split())


def normalize_word(word):
    if word == "ره":
        return "راه"
    return word


def build_network(filename, window_size, min_frequency):

    filepath = os.path.join(input_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = []

    for word in text.split():

        if word in stopwords:
            continue

        word = normalize_word(word)

        if word in keywords:
            words.append(word)

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

    return G


print()
print("=" * 70)
print("SENSITIVITY ANALYSIS")
print("=" * 70)

results = []

for window_size in window_sizes:

    for threshold in thresholds:

        print()
        print("=" * 70)
        print(
            "WINDOW SIZE =", window_size,
            "| MIN FREQUENCY =", threshold
        )
        print("=" * 70)

        for filename in files:

            G = build_network(
                filename,
                window_size,
                threshold
            )

            nodes = G.number_of_nodes()
            edges = G.number_of_edges()

            if nodes > 1:

                density = nx.density(G)

                avg_degree = (
                    sum(dict(G.degree()).values())
                    / nodes
                )

                clustering = nx.average_clustering(G)

                components = (
                    nx.number_connected_components(G)
                )

            elif nodes == 1:

                density = 0
                avg_degree = 0
                clustering = 0
                components = 1

            else:

                density = 0
                avg_degree = 0
                clustering = 0
                components = 0

            stage = filename.split(".txt_")[0]

            print(
                stage,
                "| Nodes:", nodes,
                "| Edges:", edges,
                "| Density:", round(density, 4),
                "| AvgDegree:", round(avg_degree, 4),
                "| Clustering:", round(clustering, 4),
                "| Components:", components
            )

            results.append({
                "Window_Size": window_size,
                "Min_Frequency": threshold,
                "Stage": stage,
                "Nodes": nodes,
                "Edges": edges,
                "Density": round(density, 4),
                "Average_Degree": round(avg_degree, 4),
                "Average_Clustering": round(clustering, 4),
                "Connected_Components": components
            })


with open(
    "sensitivity_analysis.csv",
    "w",
    encoding="utf-8-sig"
) as f:

    import csv

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Window_Size",
            "Min_Frequency",
            "Stage",
            "Nodes",
            "Edges",
            "Density",
            "Average_Degree",
            "Average_Clustering",
            "Connected_Components"
        ]
    )

    writer.writeheader()

    for row in results:
        writer.writerow(row)


print()
print("=" * 70)
print("SENSITIVITY ANALYSIS COMPLETE")
print("=" * 70)
print("Total configurations:", len(window_sizes) * len(thresholds))
print("Total rows:", len(results))
print("Created: sensitivity_analysis.csv")