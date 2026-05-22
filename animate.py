# ============================================================
# ANIMATION for Dijkstra's Algorithm
# This was vibe coded with help from Claude (AI).
# Our professor was okay with this since the actual algorithm
# and graph logic in dijkstra_project.py is fully ours.
# ============================================================

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx


def animate(graph, distances, previous, start, end, visit_order):

    # import the path function from the main file
    from dijkstra_project import shortest_path

    # build a networkx graph just for drawing
    G = nx.Graph()
    for v in graph.adjacency_list:
        for e in graph.adjacency_list[v]:
            G.add_edge(v, e.vertex, weight=e.distance)

    # fixed positions so the graph matches our hand-drawn diagram:
    #         D
    #        / \
    #   A---B   F
    #    \ / \ /
    #     C---E
    pos = nx.spring_layout(G, seed=42, k=2.5)
    path = shortest_path(previous, start, end)

    path_edges = set()
    for i in range(len(path) - 1):
        path_edges.add((path[i], path[i + 1]))
        path_edges.add((path[i + 1], path[i]))

    weights = nx.get_edge_attributes(G, 'weight')
    n_explore = len(visit_order)
    n_total = 2 + n_explore + 7

    fig, ax = plt.subplots(figsize=(13, 8))
    fig.patch.set_facecolor('#0a0a0a')

    def draw(frame):
        ax.clear()
        ax.set_facecolor('#0a0a0a')
        ax.axis('off')

        # frame 0: title screen
        if frame == 0:
            ax.set_title(
                f"Dijkstra's Algorithm  ·  {start}  →  {end}\n"
                f"Halmstad University  |  Group 5: Ankur Animesh & Carl Jarving",
                color='white', fontsize=15, fontweight='bold', pad=20)
            return

        # frame 1: full graph appears
        if frame == 1:
            phase        = "graph"
            explored     = set()
            current_node = None
        # frames 2 to N+1: algorithm explores one node per frame
        elif frame <= 1 + n_explore:
            phase        = "exploring"
            step_idx     = frame - 2
            explored     = set(visit_order[:step_idx])
            current_node = visit_order[step_idx]
        # remaining frames: show result
        else:
            phase        = "done"
            explored     = set(visit_order)
            current_node = None

        # --- edges ---
        all_edges   = list(G.edges())
        p_edges     = [(u, v) for u, v in all_edges if (u, v) in path_edges]
        non_p_edges = [(u, v) for u, v in all_edges if (u, v) not in path_edges]

        if phase == "graph":
            nx.draw_networkx_edges(G, pos, edge_color='#999999', width=1.8, ax=ax, alpha=0.9)
        elif phase == "done":
            if non_p_edges:
                nx.draw_networkx_edges(G, pos, edgelist=non_p_edges, edge_color='#555555', width=1.5, ax=ax)
            if p_edges:
                nx.draw_networkx_edges(G, pos, edgelist=p_edges, edge_color='#00ff44', width=5.5, ax=ax)
        else:
            nx.draw_networkx_edges(G, pos, edge_color='#2a2a2a', width=1.2, ax=ax)

        # --- nodes ---
        colors, sizes, edge_colors = [], [], []
        for n in G.nodes():
            if phase == "done" and n in path:
                colors.append('#00ff44');  sizes.append(750); edge_colors.append('#ffffff')
            elif phase == "done":
                colors.append('#666666');  sizes.append(650); edge_colors.append('#999999')
            elif phase == "exploring" and n == current_node:
                colors.append('#ff8800');  sizes.append(820); edge_colors.append('#ffffff')
            elif n in explored:
                colors.append('#007722');  sizes.append(680); edge_colors.append('#00aa44')
            elif phase == "graph":
                colors.append('#cccccc');  sizes.append(680); edge_colors.append('#ffffff')
            else:
                colors.append('#444444');  sizes.append(680); edge_colors.append('#888888')

        nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=sizes,
                               edgecolors=edge_colors, linewidths=1.8, ax=ax)

        # --- labels below nodes ---
        for node, (x, y) in pos.items():
            ax.text(x, y - 0.16, node, fontsize=11, fontweight='bold',
                    color='white', ha='center', va='top', zorder=6)

            show_cost = (
                (phase == "exploring" and (node in explored or node == current_node))
                or (phase == "done" and node in path)
            )
            if show_cost and distances[node] != float("inf"):
                ax.text(x, y + 0.17, str(distances[node]),
                        fontsize=9, color='#aaffaa', ha='center', va='bottom',
                        fontweight='bold', zorder=6)

        # --- edge weight labels ---
        for (u, v), w in weights.items():
            mx = (pos[u][0] + pos[v][0]) / 2
            my = (pos[u][1] + pos[v][1]) / 2
            ax.text(mx, my, str(w), fontsize=9, color='white',
                    ha='center', va='center', zorder=7,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#0a0a0a',
                              edgecolor='#555555', linewidth=0.8, alpha=1.0))

        # --- title ---
        if phase == "graph":
            ax.set_title(
                f"Dijkstra's Algorithm  ·  {start}  →  {end}\n"
                f"Graph ready — {len(G.nodes())} nodes, {len(G.edges())} edges  ·  Starting from {start}",
                color='white', fontsize=14, fontweight='bold', pad=15)
        elif phase == "exploring":
            ax.set_title(
                f"Dijkstra's Algorithm  ·  {start}  →  {end}\n"
                f"Step {frame-1}/{n_explore}  ·  Processing {current_node}  "
                f"(distance = {distances[current_node]})",
                color='#ff8800', fontsize=14, fontweight='bold', pad=15)
        else:
            p_str = '  →  '.join(path)
            ax.set_title(
                f"Dijkstra's Algorithm  ·  {start}  →  {end}\n"
                f"Shortest Path:  {p_str}   |   Total Distance: {distances[end]}",
                color='#00ff44', fontsize=14, fontweight='bold', pad=15)

    ani = animation.FuncAnimation(fig, draw, frames=n_total, interval=900, repeat=False)
    plt.tight_layout()
    plt.show()
