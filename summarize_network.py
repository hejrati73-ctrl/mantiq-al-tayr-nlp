import pandas as pd

df = pd.read_csv("network_results.csv")

stages = df["Stage"].unique()

for stage in stages:
    print("\n====================")
    print(stage)

    temp = df[df["Stage"] == stage]

    print("\nTop Degree:")
    print(
        temp.sort_values(
            "Degree_Centrality",
            ascending=False
        )[["Concept", "Frequency", "Degree_Centrality"]]
        .head(5)
        .to_string(index=False)
    )

    print("\nTop Betweenness:")
    print(
        temp.sort_values(
            "Betweenness",
            ascending=False
        )[["Concept", "Frequency", "Betweenness"]]
        .head(5)
        .to_string(index=False)
    )