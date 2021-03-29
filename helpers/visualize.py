import matplotlib.pyplot as plt
import numpy as np


class Visualizer:

    @staticmethod
    def compare_schedule_len(slowest_machines):
        s_lens_x = [round(m["machine"].schedule_len) for m in slowest_machines]
        labels = [m["method_used"] for m in slowest_machines]

        x = np.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots()

        rects = ax.bar(x - width / 2, s_lens_x, width)

        # plt.plot(s_lens_x, labels)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        autolabel(rects, ax)
        ax.legend()
        ax.set_ylabel("Method Used")
        # plt.grid(True)
        plt.title("Methods for multiple workflow scheduling.")
        fig.tight_layout()
        plt.show()

    @staticmethod
    def create_visuals_edges(tasks, G, go):
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))
        return edge_trace, node_trace

    @staticmethod
    def color_node_points(G, node_trace):
        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append('# of connections: ' + str(len(adjacencies[1])))

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

    """
    G = nx.Graph()
    G.add_node(task)
    G.add_nodes_from(tasks)
    G.add_edge(*edge)  (2, 3, {'weight': 3.1415})

    """
    @staticmethod
    def create_graph(tasks):
        import networkx as nx
        import random
        G = nx.DiGraph()
        random.seed(10)
        for task in tasks:
            G.add_node(task.get_key())
            for edge in task.children_edges:
                G.add_edge(task, edge.node)
        pos = {t: [10, t.level] for t in tasks}
        nx.set_node_attributes(G, pos, "pos")
        return G

    @staticmethod
    def visualize_tasks(tasks):
        import plotly.graph_objects as go
        # G = nx.random_geometric_graph(200, 10.125)

        G = Visualizer.create_graph(tasks)

        edge_trace, node_trace = Visualizer.create_visuals_edges(tasks, G, go)

        Visualizer.color_node_points(G, node_trace)

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                        title='<br>Network graph made with Python',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        fig.show()

    @staticmethod
    def visualize_machines(machines):
        import plotly.express as px
        import pandas as pd

        all_tasks = list()
        ordered_tasks = [sorted(m.tasks, key=lambda t: t.start) for m in machines]
        for tasks in ordered_tasks:
            for task in tasks:
                all_tasks.append(dict(Task=task.name, Start=task.start, Finish=task.end, Machine=task.machine_id))

        df = pd.DataFrame(all_tasks)
        df['delta'] = df['Finish'] - df['Start']

        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Machine", color="Machine")
        fig.update_yaxes(autorange="reversed")

        fig.layout.xaxis.type = 'linear'
        fig.data[0].x = df.delta.tolist()
        fig.full_figure_for_development(warn=False)
        fig.show()

    # @staticmethod
    # def visualize_schedule1(schedule):
    #     y = list()
    #     x = list()
    #     measures = list()
    #     for task in schedule["tasks"]:
    #         y.append(task.name)
    #         measures.append('relative')
    #         x.append(task.end - task.start)

    #     import plotly.graph_objects as go
    #     fig = go.Figure(go.Waterfall(
    #         name="2018", orientation="h", measure=measures,
    #         y=y,
    #         x=x,
    #         connector={"mode": "between", "line": {"width": 4, "color": "rgb(0, 0, 0)", "dash": "solid"}}
    #     ))

    #     fig.update_layout(title="Profit and loss statement 2018")

    #     fig.show()


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
