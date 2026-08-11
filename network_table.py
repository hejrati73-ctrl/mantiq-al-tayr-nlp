import pandas as pd

df = pd.read_csv("network_results.csv")

top = []

for stage in df["Stage"].unique():

    temp = df[df["Stage"] == stage]

    top5 = (
        temp.sort_values(
            "Degree_Centrality",
            ascending=False
        )
        .head(5)
    )

    for _, row in top5.iterrows():
        top.append({
            "Stage": stage,
            "Concept": row["Concept"],
            "Frequency": row["Frequency"],
            "Degree_Centrality": row["Degree_Centrality"],
            "Betweenness": row["Betweenness"]
        })


result = pd.DataFrame(top)

result.to_csv(
    "central_concepts_table.csv",
    index=False,
    encoding="utf-8-sig"
)

print("central_concepts_table.csv created!")