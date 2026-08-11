import os
import os
import pandas as pd
import matplotlib.pyplot as plt

input_file = "results/final_network_analysis_v2_en.csv"

# =========================
# Folders
# =========================

persian_folder = "comparative_figures_persian"
english_folder = "comparative_figures_english"

os.makedirs(persian_folder, exist_ok=True)
os.makedirs(english_folder, exist_ok=True)

df = pd.read_csv(input_file)

stages = [
    "Opening",
    "Birds' Journey",
    "Seven Valleys",
    "Simurgh Encounter",
    "Final State"
]

stage_labels_en = [
    "Opening",
    "Birds' Journey",
    "Seven Valleys",
    "Simurgh Encounter",
    "Final State"
]

stage_labels_fa = [
    "آغاز",
    "سفر پرندگان",
    "هفت وادی",
    "دیدار سیمرغ",
    "وضعیت نهایی"
]

concepts = [
    "جان",
    "دل",
    "راه",
    "عشق",
    "خویش",
    "درد",
    "سیمرغ"
]

concept_labels_en = {
    "جان": "Soul",
    "دل": "Heart",
    "راه": "Path",
    "عشق": "Love",
    "خویش": "Self",
    "درد": "Pain",
    "سیمرغ": "Simurgh"
}


# ============================================================
# FIGURE 1 — CONCEPTUAL CENTRALITY
# ============================================================

def make_centrality_figure(
    folder,
    language="english"
):

    plt.figure(figsize=(14, 8))

    for concept in concepts:

        data = df[df["Concept"] == concept]

        values = []

        for stage in stages:

            row = data[data["Stage"] == stage]

            if len(row) > 0:
                values.append(
                    row.iloc[0]["Degree Centrality"]
                )
            else:
                values.append(0)

        if language == "english":
            label = concept_labels_en[concept]
        else:
            label = concept

        plt.plot(
            stage_labels_en if language == "english"
            else stage_labels_fa,
            values,
            marker="o",
            label=label
        )

    if language == "english":

        plt.title(
            "Conceptual Centrality Across Narrative Stages",
            fontsize=16
        )

        plt.xlabel(
            "Narrative Stage",
            fontsize=12
        )

        plt.ylabel(
            "Degree Centrality",
            fontsize=12
        )

    else:

        plt.title(
            "مرکزیت مفاهیم در مراحل روایی",
            fontsize=16
        )

        plt.xlabel(
            "مرحله روایی",
            fontsize=12
        )

        plt.ylabel(
            "مرکزیت درجه‌ای",
            fontsize=12
        )

    plt.xticks(rotation=25)
    plt.legend()
    plt.tight_layout()

    if language == "english":
        filename = "figure_1_conceptual_centrality_EN.png"
    else:
        filename = "figure_1_conceptual_centrality_FA.png"

    plt.savefig(
        os.path.join(folder, filename),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# FIGURE 2 — NETWORK STRUCTURE
# ============================================================

def make_structure_figure(
    folder,
    language="english"
):

    network_data = (
        df.groupby("Stage")
        .first()
        .reindex(stages)
    )

    plt.figure(figsize=(14, 8))

    plt.plot(
        stage_labels_en if language == "english"
        else stage_labels_fa,
        network_data["Network Density"],
        marker="o",
        label="Density" if language == "english"
        else "چگالی"
    )

    plt.plot(
        stage_labels_en if language == "english"
        else stage_labels_fa,
        network_data["Average Degree"],
        marker="o",
        label="Average Degree" if language == "english"
        else "میانگین درجه"
    )

    plt.plot(
        stage_labels_en if language == "english"
        else stage_labels_fa,
        network_data["Clustering Coefficient"],
        marker="o",
        label="Average Clustering" if language == "english"
        else "میانگین خوشه‌بندی"
    )

    if language == "english":

        plt.title(
            "Network Structural Change Across Narrative Stages",
            fontsize=16
        )

        plt.xlabel(
            "Narrative Stage",
            fontsize=12
        )

        plt.ylabel(
            "Network Measure",
            fontsize=12
        )

    else:

        plt.title(
            "تغییر ساختار شبکه در مراحل روایتی",
            fontsize=16
        )

        plt.xlabel(
            "مرحله روایی",
            fontsize=12
        )

        plt.ylabel(
            "شاخص شبکه",
            fontsize=12
        )

    plt.xticks(rotation=25)
    plt.legend()
    plt.tight_layout()

    if language == "english":
        filename = "figure_2_network_structure_EN.png"
    else:
        filename = "figure_2_network_structure_FA.png"

    plt.savefig(
        os.path.join(folder, filename),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# FIGURE 3 — COMMUNITY STRUCTURE
# ============================================================

def make_community_figure(
    folder,
    language="english"
):

    network_data = (
        df.groupby("Stage")
        .first()
        .reindex(stages)
    )

    plt.figure(figsize=(14, 8))

    plt.plot(
        stage_labels_en if language == "english"
        else stage_labels_fa,
        network_data["Communities"],
        marker="o",
        label="Number of Communities"
        if language == "english"
        else "تعداد اجتماعات"
    )

    plt.plot(
        stage_labels_en if language == "english"
        else stage_labels_fa,
        network_data["Modularity"],
        marker="o",
        label="Modularity"
        if language == "english"
        else "مدولاریتی"
    )

    if language == "english":

        plt.title(
            "Community Structure Across Narrative Stages",
            fontsize=16
        )

        plt.xlabel(
            "Narrative Stage",
            fontsize=12
        )

        plt.ylabel(
            "Value",
            fontsize=12
        )

    else:

        plt.title(
            "ساختار اجتماعات در مراحل روایتی",
            fontsize=16
        )

        plt.xlabel(
            "مرحله روایی",
            fontsize=12
        )

        plt.ylabel(
            "مقدار",
            fontsize=12
        )

    plt.xticks(rotation=25)
    plt.legend()
    plt.tight_layout()

    if language == "english":
        filename = "figure_3_community_structure_EN.png"
    else:
        filename = "figure_3_community_structure_FA.png"

    plt.savefig(
        os.path.join(folder, filename),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# CREATE BOTH VERSIONS
# ============================================================

make_centrality_figure(
    english_folder,
    "english"
)

make_structure_figure(
    english_folder,
    "english"
)

make_community_figure(
    english_folder,
    "english"
)


make_centrality_figure(
    persian_folder,
    "persian"
)

make_structure_figure(
    persian_folder,
    "persian"
)

make_community_figure(
    persian_folder,
    "persian"
)


print("\nAll comparative figures created successfully!")

print("\nEnglish figures:")
for file in os.listdir(english_folder):
    print(" ", file)

print("\nPersian figures:")
for file in os.listdir(persian_folder):
    print(" ", file)
