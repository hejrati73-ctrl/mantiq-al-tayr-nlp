import os
import csv
from collections import Counter

input_folder = "sections"

files = [
    ("Opening", "opening.txt_01"),
    ("Birds' Journey", "birds_journey.txt_02"),
    ("Seven Valleys", "seven_valleys.txt_03"),
    ("Simurgh Encounter", "simurgh_encounter.txt_04"),
    ("Final State", "final_state.txt_05")
]

window_size = 5

keywords = {
    "جان", "دل", "خویش", "راه", "ره", "عشق", "طلب", "درد",
    "سیمرغ", "مرغ", "محو", "فنا", "بقا", "خاک", "تن",
    "جسم", "پاک", "عقل", "نفس"
}

normalization = {
    "ره": "راه"
}

concepts = [
    "جان", "دل", "خویش", "راه", "عشق", "طلب", "درد",
    "سیمرغ", "مرغ", "محو", "فنا", "بقا", "خاک", "تن",
    "جسم", "پاک", "عقل", "نفس"
]

print("=" * 80)
print("PMI RAW STATISTICS AUDIT")
print("=" * 80)

for stage, filename in files:

    filepath = os.path.join(input_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    raw_words = text.split()

    words = [
        normalization.get(w, w)
        for w in raw_words
    ]

    N_words = len(words)

    # Number of sliding windows
    N_windows = N_words

    # Single concept frequencies
    concept_frequency = Counter(
        w for w in words
        if w in concepts
    )

    # Pair frequencies — EXACTLY same logic as PMI script
    pair_frequency = Counter()

    for i in range(N_words):

        window_end = min(
            i + window_size,
            N_words
        )

        window = words[i:window_end]

        concepts_in_window = [
            w for w in window
            if w in concepts
        ]

        # Each concept counted once per window
        unique_concepts = list(
            dict.fromkeys(concepts_in_window)
        )

        for a in range(len(unique_concepts)):

            for b in range(a + 1, len(unique_concepts)):

                w1 = unique_concepts[a]
                w2 = unique_concepts[b]

                pair = tuple(sorted((w1, w2)))

                pair_frequency[pair] += 1

    print()
    print("-" * 80)
    print(stage)
    print("-" * 80)

    print("N_words:", N_words)
    print("N_windows:", N_windows)

    print()
    print("CONCEPT FREQUENCIES")
    print("-------------------")

    for concept in concepts:
        print(
            f"{concept}: {concept_frequency.get(concept, 0)}"
        )

    print()
    print("PAIR FREQUENCIES")
    print("----------------")

    for (w1, w2), count in sorted(pair_frequency.items()):

        if count > 0:
            print(
                f"{w1} -- {w2}: {count}"
            )

print()
print("=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)