import os
import csv
import networkx as nx
from collections import Counter

input_folder = "sections"

output_file_fa = "final_results_table_fa.csv"
output_file_en = "final_results_table_en.csv"

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


stage_names_fa = {
    "opening": "آغاز",
    "birds_journey": "سفر مرغان",
    "seven_valleys": "هفت وادی",
    "simurgh_encounter": "دیدار سیمرغ",
    "final_state": "وضعیت نهایی"
}

stage_names_en = {
    "opening": "Opening",
    "birds_journey": "Birds' Journey",
    "seven_valleys": "Seven Valleys",
    "simurgh_encounter": "Simurgh Encounter",
    "final_state": "Final State"
}

rows_fa = []
rows_en = []

for filename in files:

    stage = filename.split(".txt_")[0]

    G = build_network(filename)

    if G.number_of_nodes() == 0:
        continue

    density = nx.density(G)

    average_degree = (
        sum(dict(G.degree()).values())
        / G.number_of_nodes()
    )

    clustering = nx.average_clustering(G)

    components = nx.number_connected_components(G)

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

    rows_fa.append([
        stage_names_fa[stage],
        G.number_of_nodes(),
        G.number_of_edges(),
        round(density, 4),
        round(average_degree, 4),
        round(clustering, 4),
        components,
        len(communities),
        round(modularity, 4)
    ])

    rows_en.append([
        stage_names_en[stage],
        G.number_of_nodes(),
        G.number_of_edges(),
        round(density, 4),
        round(average_degree, 4),
        round(clustering, 4),
        components,
        len(communities),
        round(modularity, 4)
    ])


headers_fa = [
    "مرحله",
    "تعداد گره‌ها",
    "تعداد یال‌ها",
    "چگالی شبکه",
    "میانگین درجه",
    "میانگین خوشه‌بندی",
    "تعداد مؤلفه‌های همبند",
    "تعداد اجتماعات",
    "مدولاریتی"
]

headers_en = [
    "Stage",
    "Nodes",
    "Edges",
    "Density",
    "Average Degree",
    "Average Clustering",
    "Connected Components",
    "Number of Communities",
    "Modularity"
]


with open(
    output_file_fa,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.writer(f)
    writer.writerow(headers_fa)
    writer.writerows(rows_fa)


with open(
    output_file_en,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.writer(f)
    writer.writerow(headers_en)
    writer.writerows(rows_en)


print()
print("=" * 70)
print("FINAL RESULTS TABLE")
print("=" * 70)

for row in rows_en:
    print(row)

print()
print("Created:")
print(output_file_fa)
print(output_file_en)