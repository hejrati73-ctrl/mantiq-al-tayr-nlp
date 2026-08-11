import os
import csv
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

keywords = {
    "جان",
    "دل",
    "خویش",
    "راه",
    "ره",
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

window_size = 5
min_frequency = 15

results = []


for filename in files:

    filepath = os.path.join(input_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = [
        w for w in text.split()
        if w in keywords
    ]

    frequency = Counter(words)

    pairs = Counter()

    for i in range(len(words)):
        window = words[i:i+window_size]

        for w1 in window:
            for w2 in window:
                if w1 < w2:
                    pairs[(w1, w2)] += 1


    G = nx.Graph()

    for (w1, w2), count in pairs.items():
        if count >= min_frequency:
            G.add_edge(w1, w2, weight=count)


    degree = nx.degree_centrality(G)
    between = nx.betweenness_centrality(G)


    stage = filename.split(".")[0]


    for word in G.nodes():

        results.append([
            stage,
            word,
            frequency[word],
            round(degree[word], 4),
            round(between[word], 4)
        ])


with open(
    "network_results.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "Stage",
        "Concept",
        "Frequency",
        "Degree_Centrality",
        "Betweenness"
    ])

    writer.writerows(results)


print("network_results.csv created!")