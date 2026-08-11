import pandas as pd
import networkx as nx

# 1. Load Edge Evolution Data
df_edges = pd.read_csv('normalized_edge_evolution_long.csv')

# Dynamically identify column names
cols = df_edges.columns.tolist()
stage_col = [c for c in cols if 'stage' in c.lower()][0]
cols_rem = [c for c in cols if c != stage_col]
source_col = cols_rem[0]
target_col = cols_rem[1]

stages = df_edges[stage_col].unique()
results = []

for stage in stages:
    stage_df = df_edges[df_edges[stage_col] == stage]
    G = nx.Graph()
    
    for _, row in stage_df.iterrows():
        u, v = str(row[source_col]).strip(), str(row[target_col]).strip()
        G.add_edge(u, v)
        
    deg_cent = nx.degree_centrality(G)
    bet_cent = nx.betweenness_centrality(G)
    clo_cent = nx.closeness_centrality(G)
    
    try:
        eig_cent = nx.eigenvector_centrality(G, max_iter=1000)
    except:
        eig_cent = {node: 0.0 for node in G.nodes()}
        
    for node in G.nodes():
        results.append({
            'Stage': stage,
            'Concept': node,
            'Degree': G.degree(node),
            'Degree_Centrality': round(deg_cent[node], 4),
            'Betweenness_Centrality': round(bet_cent[node], 4),
            'Closeness_Centrality': round(clo_cent[node], 4),
            'Eigenvector_Centrality': round(eig_cent[node], 4)
        })

df_out = pd.DataFrame(results)
df_out.to_csv('node_centrality_trajectories.csv', index=False, encoding='utf-8-sig')
print("Successfully generated: node_centrality_trajectories.csv")
print(f"Total records exported: {len(df_out)}")