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


def build_network(filename):

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
            G.add_edge(w1, w2, weight=count)

    return G


for filename in files:

    G = build_network(filename)

    print("\n====================")
    print(filename)

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    if G.number_of_nodes() > 2:

        communities = nx.community.greedy_modularity_communities(
            G,
            weight="weight"
        )

        modularity = nx.community.modularity(
            G,
            communities,
            weight="weight"
        )

        print("Number of communities:", len(communities))
        print("Modularity:", round(modularity, 4))

        sorted_communities = sorted(
            communities,
            key=len,
            reverse=True
        )

        for i, community in enumerate(sorted_communities, 1):

            members = sorted(community)

            print(
                f"\nCommunity {i} "
                f"({len(members)} nodes):"
            )

            print(" | ".join(members))

    else:

        print("Network too small for community detection.")