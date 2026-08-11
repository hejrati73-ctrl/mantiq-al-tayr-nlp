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
                    pairs[(w1,w2)] += 1


    G = nx.Graph()

    for (w1,w2),count in pairs.items():
        if count >= min_frequency:
            G.add_edge(w1,w2,weight=count)


    centrality = nx.degree_centrality(G)


    print("\n====================")
    print(filename)

    print("\nFrequency:")
    for word,count in frequency.most_common(5):
        print(word, count)


    print("\nNetwork:")
    for word,score in sorted(
        centrality.items(),
        key=lambda x:x[1],
        reverse=True
    )[:5]:
        print(word, round(score,3))