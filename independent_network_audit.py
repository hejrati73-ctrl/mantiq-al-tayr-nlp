import os
import pandas as pd
import networkx as nx
from collections import Counter

# ============================================================
# INDEPENDENT NETWORK AUDIT
# Rebuild networks directly from raw section files
# ============================================================

INPUT_FOLDER = "sections"
WINDOW_SIZE = 5
MIN_FREQUENCY = 15

FILES = [
    ("Opening", "opening.txt_01"),
    ("Birds' Journey", "birds_journey.txt_02"),
    ("Seven Valleys", "seven_valleys.txt_03"),
    ("Simurgh Encounter", "simurgh_encounter.txt_04"),
    ("Final State", "final_state.txt_05"),
]

KEYWORDS = {
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
    "نفس",
}


def build_network(text):
    words = [w for w in text.split() if w in KEYWORDS]

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
            G.add_edge(w1, w2, weight=count)

    return words, pairs, G


print("=" * 75)
print("INDEPENDENT NETWORK AUDIT")
print("=" * 75)

results = []

for stage, filename in FILES:

    filepath = os.path.join(INPUT_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words, pairs, G = build_network(text)

    nodes = G.number_of_nodes()
    edges = G.number_of_edges()

    density = nx.density(G) if nodes > 1 else 0
    average_degree = (
        sum(dict(G.degree()).values()) / nodes
        if nodes > 0 else 0
    )

    components = nx.number_connected_components(G) if nodes > 0 else 0

    print(f"\n{stage}")
    print("-" * 50)
    print("Concept tokens:", len(words))
    print("Unique co-occurring pairs:", len(pairs))
    print("Nodes:", nodes)
    print("Edges:", edges)
    print("Density:", round(density, 4))
    print("Average Degree:", round(average_degree, 4))
    print("Connected Components:", components)

    results.append({
        "Stage": stage,
        "Nodes": nodes,
        "Edges": edges,
        "Density": round(density, 4),
        "Average_Degree": round(average_degree, 4),
        "Connected_Components": components,
    })


# ------------------------------------------------------------
# Save independent results
# ------------------------------------------------------------

audit_df = pd.DataFrame(results)

audit_df.to_csv(
    "independent_network_audit.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 75)
print("AUDIT TABLE")
print("=" * 75)
print(audit_df.to_string(index=False))

# ------------------------------------------------------------
# Compare against existing stage metrics
# ------------------------------------------------------------

reference_file = "stage_network_metrics_en.csv"

if os.path.exists(reference_file):

    ref = pd.read_csv(reference_file)

    merged = audit_df.merge(
        ref,
        on="Stage",
        suffixes=("_Independent", "_Reference")
    )

    print("\n" + "=" * 75)
    print("COMPARISON WITH EXISTING NETWORK METRICS")
    print("=" * 75)

    checks = {
        "Nodes": (
            merged["Nodes_Independent"]
            == merged["Nodes_Reference"]
        ),
        "Edges": (
            merged["Edges_Independent"]
            == merged["Edges_Reference"]
        ),
        "Density": (
            abs(
                merged["Density_Independent"]
                - merged["Density_Reference"]
            ) < 1e-4
        ),
        "Average Degree": (
            abs(
                merged["Average_Degree_Independent"]
                - merged["Average_Degree_Reference"]
            ) < 1e-4
        ),
        "Connected Components": (
            merged["Connected_Components_Independent"]
            == merged["Connected_Components_Reference"]
        ),
    }

    for name, result in checks.items():
        print(
            f"{name:25} "
            f"{'PASS' if result.all() else 'FAIL'}"
        )

    if all(result.all() for result in checks.values()):
        print("\nOVERALL RESULT: PASS")
        print("Independent reconstruction matches the reference metrics.")
    else:
        print("\nOVERALL RESULT: FAIL")
        print("At least one metric differs.")

else:
    print(
        "\nReference file stage_network_metrics_en.csv "
        "was not found."
    )