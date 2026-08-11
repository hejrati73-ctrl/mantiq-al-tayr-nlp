import os
import math
import csv
from collections import Counter

input_folder = "sections"

files = [
    "opening.txt_01",
    "birds_journey.txt_02",
    "seven_valleys.txt_03",
    "simurgh_encounter.txt_04",
    "final_state.txt_05"
]

stage_names_fa = {
    "opening": "آغاز",
    "birds_journey": "سفر پرندگان",
    "seven_valleys": "هفت وادی",
    "simurgh_encounter": "دیدار سیمرغ",
    "final_state": "حالت نهایی"
}

stage_names_en = {
    "opening": "Opening",
    "birds_journey": "Birds' Journey",
    "seven_valleys": "Seven Valleys",
    "simurgh_encounter": "Simurgh Encounter",
    "final_state": "Final State"
}

window_size = 5
min_frequency = 15

keywords = {
    "جان", "دل", "خویش", "راه", "ره", "عشق",
    "طلب", "درد", "سیمرغ", "مرغ", "محو", "فنا",
    "بقا", "خاک", "تن", "جسم", "پاک", "عقل", "نفس"
}


def normalize_word(word):
    if word == "ره":
        return "راه"
    return word


def load_text(filename):

    filepath = os.path.join(input_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def prepare_text(text):

    raw_words = text.split()

    normalized_words = [
        normalize_word(word)
        for word in raw_words
    ]

    return normalized_words


def calculate_pmi(words):

    # Frequency of target concepts in the complete text
    concept_frequency = Counter(
        word for word in words
        if word in keywords
    )

    # Number of all tokens in the actual text
    total_tokens = len(words)

    pair_frequency = Counter()

    # IMPORTANT:
    # We keep the original text positions.
    # Non-keywords are NOT removed before creating windows.

    for i in range(total_tokens):

        window_end = min(
            i + window_size,
            total_tokens
        )

        window = words[i:window_end]

        concepts_in_window = [
            word for word in window
            if word in keywords
        ]

        unique_concepts = list(
            dict.fromkeys(concepts_in_window)
        )

        for a in range(len(unique_concepts)):

            for b in range(a + 1, len(unique_concepts)):

                w1 = unique_concepts[a]
                w2 = unique_concepts[b]

                pair = tuple(sorted((w1, w2)))

                pair_frequency[pair] += 1

    results = []

    for (w1, w2), pair_count in pair_frequency.items():

        if pair_count < min_frequency:
            continue

        f1 = concept_frequency[w1]
        f2 = concept_frequency[w2]

        if f1 == 0 or f2 == 0:
            continue

        # Probability estimates
        p_w1 = f1 / total_tokens
        p_w2 = f2 / total_tokens
        p_pair = pair_count / total_tokens

        if p_pair <= 0:
            continue

        pmi = math.log2(
            p_pair / (p_w1 * p_w2)
        )

        results.append({
            "Word1": w1,
            "Word2": w2,
            "Pair_Frequency": pair_count,
            "PMI": round(pmi, 4)
        })

    results.sort(
        key=lambda x: x["PMI"],
        reverse=True
    )

    return results


all_results_fa = []
all_results_en = []

print()
print("=" * 70)
print("PMI ANALYSIS")
print("=" * 70)

for filename in files:

    stage_key = filename.split(".txt_")[0]

    text = load_text(filename)
    words = prepare_text(text)

    results = calculate_pmi(words)

    print()
    print("=" * 70)
    print(stage_names_en[stage_key])
    print("=" * 70)

    print("Total tokens:", len(words))
    print("Relationships analyzed:", len(results))

    print()
    print("TOP PMI RELATIONSHIPS")
    print("---------------------")

    for row in results[:10]:

        print(
            row["Word1"],
            "--",
            row["Word2"],
            "| Frequency:",
            row["Pair_Frequency"],
            "| PMI:",
            row["PMI"]
        )

        all_results_fa.append({
            "مرحله": stage_names_fa[stage_key],
            "مفهوم ۱": row["Word1"],
            "مفهوم ۲": row["Word2"],
            "فراوانی هم‌رخدادی": row["Pair_Frequency"],
            "PMI": row["PMI"]
        })

        all_results_en.append({
            "Stage": stage_names_en[stage_key],
            "Concept 1": row["Word1"],
            "Concept 2": row["Word2"],
            "Co-occurrence Frequency": row["Pair_Frequency"],
            "PMI": row["PMI"]
        })


# ---------------------------------------------------------
# Persian CSV
# ---------------------------------------------------------

with open(
    "pmi_analysis_fa.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "مرحله",
            "مفهوم ۱",
            "مفهوم ۲",
            "فراوانی هم‌رخدادی",
            "PMI"
        ]
    )

    writer.writeheader()
    writer.writerows(all_results_fa)


# ---------------------------------------------------------
# English CSV
# ---------------------------------------------------------

with open(
    "pmi_analysis_en.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Stage",
            "Concept 1",
            "Concept 2",
            "Co-occurrence Frequency",
            "PMI"
        ]
    )

    writer.writeheader()
    writer.writerows(all_results_en)


print()
print("=" * 70)
print("PMI ANALYSIS COMPLETE")
print("=" * 70)

print("Created:")
print("pmi_analysis_fa.csv")
print("pmi_analysis_en.csv")

print()
print("Window size:", window_size)
print("Minimum frequency:", min_frequency)
print("Original token positions preserved.")