import os
import networkx as nx
from collections import Counter

INPUT_FOLDER = "sections"

FILES = [
    "opening.txt_01",
    "birds_journey.txt_02",
    "seven_valleys.txt_03",
    "simurgh_encounter.txt_04",
    "final_state.txt_05"
]

WINDOW_SIZE = 5
MIN_FREQUENCY = 15

KEYWORDS = {
    "جان", "دل", "خویش", "راه", "عشق", "طلب", "درد",
    "سیمرغ", "مرغ", "محو", "فنا", "بقا", "خاک", "تن",
    "جسم", "پاک", "عقل", "نفس"
}

NORMALIZATION = {
    "ره": "راه"
}

print("=" * 70)
print("FINAL PIPELINE AUDIT")
print("=" * 70)

# --------------------------------------------------
# Build network
# --------------------------------------------------

def build_network(filename):

    filepath = os.path.join(INPUT_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = []

    for word in text.split():

        # Normalize before filtering
        if word in NORMALIZATION:
            word = NORMALIZATION[word]

        if word not in stopwords and word in KEYWORDS:
            words.append(word)

    frequency = Counter(words)

    pairs = Counter()

    for i in range(len(words)):

        window = words[i:i + WINDOW_SIZE]

        for a in range(len(window)):

            for b in range(a + 1, len(window)):

                w1 = window[a]
                w2 = window[b]

                if w1 != w2:

                    pair = tuple(sorted((w1, w2)))
                    pairs[pair] += 1

    G = nx.Graph()

    for (w1, w2), count in pairs.items():

        if count >= MIN_FREQUENCY:

            G.add_edge(
                w1,
                w2,
                weight=count
            )

    return G, frequency


# --------------------------------------------------
# Stopwords
# --------------------------------------------------

with open(
    "persian_stopwords.txt",
    "r",
    encoding="utf-8"
) as f:

    stopwords = set(f.read().split())


# --------------------------------------------------
# Audit every stage
# --------------------------------------------------

for filename in FILES:

    stage = filename.split(".txt_")[0]

    G, frequency = build_network(filename)

    print("\n" + "=" * 70)
    print(stage)
    print("=" * 70)

    # Basic structure

    nodes = G.number_of_nodes()
    edges = G.number_of_edges()

    density = nx.density(G)

    average_degree = (
        sum(dict(G.degree()).values()) / nodes
        if nodes > 0
        else 0
    )

    clustering = (
        nx.average_clustering(G)
        if nodes > 0
        else 0
    )

    components = (
        nx.number_connected_components(G)
        if nodes > 0
        else 0
    )

    # Communities

    if nodes >= 3:

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

    else:

        communities = []
        modularity = 0

    # Centrality

    if nodes > 0:

        degree = nx.degree_centrality(G)

        betweenness = nx.betweenness_centrality(G)

    else:

        degree = {}
        betweenness = {}

    # --------------------------------------------------
    # Print metrics
    # --------------------------------------------------

    print("Nodes:", nodes)
    print("Edges:", edges)
    print("Density:", round(density, 4))
    print("Average Degree:", round(average_degree, 4))
    print("Average Clustering:", round(clustering, 4))
    print("Connected Components:", components)

    print(
        "Number of Communities:",
        len(communities)
    )

    print(
        "Modularity:",
        round(modularity, 4)
    )

    # --------------------------------------------------
    # Normalization check
    # --------------------------------------------------

    if "ره" in G.nodes():

        print("WARNING: ره is still present!")

    else:

        print("Normalization check: PASS")

    # --------------------------------------------------
    # Top Degree
    # --------------------------------------------------

    print("\nTop Degree:")

    for concept, score in sorted(
        degree.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]:

        print(
            concept,
            round(score, 4)
        )

    # --------------------------------------------------
    # Top Betweenness
    # --------------------------------------------------

    print("\nTop Betweenness:")

    for concept, score in sorted(
        betweenness.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]:

        print(
            concept,
            round(score, 4)
        )

    # --------------------------------------------------
    # Communities
    # --------------------------------------------------

    print("\nCommunities:")

    for i, community in enumerate(
        communities,
        start=1
    ):

        print(
            f"Community {i}:"
        )

        print(
            " | ".join(
                sorted(community)
            )
        )


# --------------------------------------------------
# Final checks
# --------------------------------------------------

print("\n")
print("=" * 70)
print("GLOBAL CHECKS")
print("=" * 70)

print("Window size:", WINDOW_SIZE)
print("Minimum frequency:", MIN_FREQUENCY)

print(
    "Normalization:",
    "ره -> راه"
)

print(
    "Number of stages:",
    len(FILES)
)

print("\nAudit completed successfully.")
print("No files were modified.")