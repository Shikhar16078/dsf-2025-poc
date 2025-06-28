import networkx as nx
import matplotlib.pyplot as plt

edges = [
    ("CS010A", "CS010B"),
    ("CS010B", "CS010C"),
    ("CS010C", "CS141"),
    ("CS141", "CS161"),
    ("CS141", "CS153"),
    ("CS141", "CS150"),
    ("CS141", "CS152"),
    ("CS150", "CS152"),
    ("CS161", "CS301"),
    ("CS153", "CS160"),
    ("CS010C", "CS100"),
    ("CS010C", "CS111"),
]

prereqs = [
    ("CS010A", "CS010B"),
    ("CS010B", "CS010C"),
    ("CS010C", "CS141"),
    ("CS141", "CS161"),
    ("CS141", "CS153"),
    ("CS141", "CS150"),
    ("CS150", "CS152"),
    ("CS161", "CS301"),
    ("CS153", "CS160"),
    ("CS010C", "CS100"),
    ("CS010C", "CS111"),
]

G = nx.DiGraph()
G.add_edges_from(prereqs)

topo_order = list(nx.topological_sort(G))
print("Topological Course Order:")
print(" → ".join(topo_order))

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, arrows=True, node_color='lightblue', node_size=2500, font_size=10, font_weight='bold')
plt.title("UCR Computer Science Degree Prerequisite DAG")
plt.tight_layout()
plt.show()
