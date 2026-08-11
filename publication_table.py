import csv

input_file = "final_network_analysis.csv"
output_file = "publication_table.csv"

stages = [
    "opening",
    "birds_journey",
    "seven_valleys",
    "simurgh_encounter",
    "final_state"
]

stage_labels = {
    "opening": "Opening",
    "birds_journey": "Birds' Journey",
    "seven_valleys": "Seven Valleys",
    "simurgh_encounter": "Simurgh Encounter",
    "final_state": "Final State"
}

data = {}

with open(input_file, "r", encoding="utf-8-sig") as f:

    reader = csv.DictReader(f)

    for row in reader:

        stage = row["Stage"]

        if stage not in data:

            data[stage] = {
                "Nodes": row.get("Nodes", ""),
                "Edges": row.get("Edges", ""),
                "Density": row.get("Density", ""),
                "Average_Degree": row.get("Average_Degree", ""),
                "Average_Clustering": row.get("Average_Clustering", ""),
                "Components": row.get("Connected_Components", ""),
                "Communities": row.get("Communities", ""),
                "Modularity": row.get("Modularity", "")
            }


with open(
    output_file,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "Stage",
        "Nodes",
        "Edges",
        "Density",
        "Average Degree",
        "Average Clustering",
        "Connected Components",
        "Communities",
        "Modularity"
    ])

    for stage in stages:

        writer.writerow([
            stage_labels[stage],
            data[stage]["Nodes"],
            data[stage]["Edges"],
            data[stage]["Density"],
            data[stage]["Average_Degree"],
            data[stage]["Average_Clustering"],
            data[stage]["Components"],
            data[stage]["Communities"],
            data[stage]["Modularity"]
        ])


print("Publication table created successfully.")