import os
import networkx as nx
import matplotlib.pyplot as plt
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

with open("persian_stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(f.read().split())

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


for filename in files:

    filepath = os.path.join(input_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = [
        w for w in text.split()
        if w not in stopwords
    ]

    words = [
        w for w in words
        if w in keywords
    ]

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


    plt.figure(figsize=(12, 10))

    pos = nx.spring_layout(G, k=0.5)

    nx.draw_networkx(
        G,
        pos,
        with_labels=True,
        node_size=800,
        font_size=10
    )

    plt.title(filename)

    output_name = filename.replace(".txt_0", "_network") + ".png"

    plt.savefig(output_name, dpi=300, bbox_inches="tight")
    plt.close()


print("All networks created!")