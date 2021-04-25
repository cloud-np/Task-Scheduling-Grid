import matplotlib.pyplot as plt
from typing import Dict, List
import plotly.graph_objects as go
import numpy as np


class Visualizer:

    @staticmethod
    def compare_schedule_len(slowest_machines, n_workflows):
        s_lens_x = [round(m["machine"].schedule_len) for m in slowest_machines]
        labels = [m["method_used"] for m in slowest_machines]

        plt.style.use("seaborn-dark")
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
        plt.title(f"Multiple workflow scheduling sample size {n_workflows}")
        plt.grid(True)
        fig.tight_layout()
        plt.show()

    @staticmethod
    def compare_hole_filling_methods(slowest_machines):

        methods_order = list()
        infos: Dict[str, List[int]] = dict()
        for i, m in enumerate(slowest_machines):
            ttypes, method = m['method_used'].split()
            if i < 4:
                methods_order.append(method)
            if infos.get(ttypes) is not None:
                infos[ttypes].append(round(m['machine'].schedule_len))
            else:
                infos[ttypes] = [round(m['machine'].schedule_len)]

        bars = list()
        for key, info in infos.items():
            bars.append(go.Bar(name=key, x=methods_order, y=info))  # type:ignore

        fig = go.Figure(data=bars)  # type: ignore

        # fig = go.Figure(data=[
        #     go.Bar(name='SF Zoo', x=fill_methods, y=[20, 14, 23]),  # type:ignore
        #     go.Bar(name='LA Zoo', x=fill_methods, y=[12, 18, 29])   # type:ignore
        # ])
        # Change the bar mode
        fig.update_layout(barmode='group')
        fig.show()

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
    def visualize_machines(machines):
        import plotly.express as px
        import pandas as pd

        all_tasks = list()
        ordered_tasks = [sorted(m.tasks, key=lambda t: t.start) for m in machines]
        for tasks in ordered_tasks:
            for task in tasks:
                slp = task.slowest_parent if task.slowest_parent is not None else {'parent_task': None, 'cummonication_time': -1}
                all_tasks.append(
                    dict(
                        TaskName=task.name,
                        SlowestParent=f"{slp['parent_task'].name if slp['parent_task'] is not None else 'None'} "
                                      f" w: {slp['communication_time']}",
                        Start=task.start, Finish=task.end, Machine=f"M-{task.machine_id}", WF_ID=task.wf_id))
                # all_tasks.append(dict(Task=task.name, Start=task.start, Finish=task.end, Machine=f"{task.machine_id} - T[{task.name}]", WF_ID=task.wf_id))

        df = pd.DataFrame(all_tasks)
        df['delta'] = df['Finish'] - df['Start']

        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Machine", hover_data=["TaskName", "SlowestParent"], color="WF_ID")
        fig.update_yaxes(autorange="reversed")

        fig.layout.xaxis.type = 'linear'
        fig.data[0].x = df.delta.tolist()
        fig.full_figure_for_development(warn=False)
        fig.show()


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
