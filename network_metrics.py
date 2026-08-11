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

window_size = 5
min_frequency = 15

keywords = {
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
}

normalization = {
    "ره": "راه"
}


for filename in files:

    filepath = os.path.join(input_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = []

    for w in text.split():

        if w in normalization:
            w = normalization[w]

        if w in keywords:
            words.append(w)

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

    print("\n====================")
    print(filename)

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    if G.number_of_nodes() > 1:

        density = nx.density(G)

        average_degree = (
            sum(dict(G.degree()).values())
            / G.number_of_nodes()
        )

        clustering = nx.average_clustering(G)

        components = nx.number_connected_components(G)

        print("Density:", round(density, 4))
        print("Average Degree:", round(average_degree, 4))
        print("Average Clustering:", round(clustering, 4))
        print("Connected Components:", components)

        degree = nx.degree_centrality(G)

        print("\nTop Degree:")

        for word, score in sorted(
            degree.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:

            print(
                word,
                round(score, 3)
            )

        if G.number_of_nodes() > 2:

            betweenness = nx.betweenness_centrality(G)

            print("\nTop Betweenness:")

            for word, score in sorted(
                betweenness.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]:

                print(
                    word,
                    round(score, 3)
                )

    else:

        print("Network too small for metrics.")