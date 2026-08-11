import os
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

input_folder = "sections"

output_folder_fa = "community_networks_fa"
output_folder_en = "community_networks_en"

os.makedirs(output_folder_fa, exist_ok=True)
os.makedirs(output_folder_en, exist_ok=True)

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

with open("persian_stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(f.read().split())


stage_names_fa = {
    "opening.txt_01": "آغاز",
    "birds_journey.txt_02": "سفر پرندگان",
    "seven_valleys.txt_03": "هفت وادی",
    "simurgh_encounter.txt_04": "دیدار سیمرغ",
    "final_state.txt_05": "وضعیت نهایی"
}

stage_names_en = {
    "opening.txt_01": "Opening",
    "birds_journey.txt_02": "Birds' Journey",
    "seven_valleys.txt_03": "Seven Valleys",
    "simurgh_encounter.txt_04": "Simurgh Encounter",
    "final_state.txt_05": "Final State"
}

concepts_en = {
    "جان": "Soul",
    "دل": "Heart",
    "خویش": "Self",
    "راه": "Path",
    "عشق": "Love",
    "طلب": "Quest",
    "درد": "Pain",
    "سیمرغ": "Simurgh",
    "مرغ": "Bird",
    "محو": "Annihilation",
    "فنا": "Fana",
    "بقا": "Baqa",
    "خاک": "Dust",
    "تن": "Body",
    "جسم": "Body",
    "پاک": "Purity",
    "عقل": "Intellect",
    "نفس": "Ego"
}


def build_network(filename):

    filepath = os.path.join(input_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = []

    for w in text.split():

        if w in normalization:
            w = normalization[w]

        if w not in stopwords and w in keywords:
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

    return G


for filename in files:

    G = build_network(filename)

    if G.number_of_nodes() < 3:
        continue

    communities = list(
        nx.community.greedy_modularity_communities(
            G,
            weight="weight"
        )
    )

    degree = nx.degree_centrality(G)

    node_sizes = [
        500 + degree[node] * 1800
        for node in G.nodes()
    ]

    edge_widths = [
        max(0.5, G[u][v]["weight"] * 0.08)
        for u, v in G.edges()
    ]

    pos = nx.spring_layout(
        G,
        k=0.8,
        seed=42,
        weight="weight"
    )

    # ==================================================
    # Persian version
    # ==================================================

    plt.figure(figsize=(14, 11))

    for community in communities:

        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=list(community),
            node_size=[
                node_sizes[list(G.nodes()).index(node)]
                for node in community
            ],
            alpha=0.9
        )

    nx.draw_networkx_edges(
        G,
        pos,
        width=edge_widths,
        alpha=0.45
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=12
    )

    plt.title(
        stage_names_fa[filename],
        fontsize=18
    )

    plt.axis("off")

    output_path_fa = os.path.join(
        output_folder_fa,
        filename.replace(".txt_", "_community_network_fa_") + ".png"
    )

    plt.savefig(
        output_path_fa,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Created FA:", output_path_fa)

    # ==================================================
    # English version
    # ==================================================

    plt.figure(figsize=(14, 11))

    for community in communities:

        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=list(community),
            node_size=[
                node_sizes[list(G.nodes()).index(node)]
                for node in community
            ],
            alpha=0.9
        )

    nx.draw_networkx_edges(
        G,
        pos,
        width=edge_widths,
        alpha=0.45
    )

    english_labels = {
        node: concepts_en.get(node, node)
        for node in G.nodes()
    }

    nx.draw_networkx_labels(
        G,
        pos,
        labels=english_labels,
        font_size=12
    )

    plt.title(
        stage_names_en[filename],
        fontsize=18
    )

    plt.axis("off")

    output_path_en = os.path.join(
        output_folder_en,
        filename.replace(".txt_", "_community_network_en_") + ".png"
    )

    plt.savefig(
        output_path_en,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Created EN:", output_path_en)


print("\nAll community networks created!")