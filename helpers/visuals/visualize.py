import matplotlib.pyplot as plt
from typing import Dict, List
import plotly.graph_objects as go
import numpy as np


class Visualizer:

    @staticmethod
    def compare_data(data, methods_used, n_workflows, save_fig=False, show_fig=True):
        data_on_x: List[int] = [round(d) for d in data]

        # Change the color of the smallest schedule_len
        bar_colors = ['b' for _ in data_on_x]
        min_len_index = data_on_x.index(min(data_on_x))
        bar_colors[min_len_index] = 'r'

        labels = list(methods_used)

        plt.style.use("seaborn-dark")
        x = np.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots()

        rects = ax.bar(x - width / 2, data_on_x, width, color=bar_colors)

        plt.xticks(x, rotation='vertical')
        ax.set_xticklabels(labels)
        # autolabel(rects, ax)
        ax.legend()
        ax.set_ylabel("Method Used")
        # plt.grid(True)
        plt.title(f"Multiple workflow scheduling sample size {n_workflows}")
        plt.grid(True)
        fig.set_size_inches(12, 4)
        fig.tight_layout()

        if show_fig:
            plt.show()
        if save_fig:
            plt.savefig("fig")
        return fig

    @staticmethod
    def compare_hole_filling_methods(data):

        methods_order = []
        infos: Dict[str, List[int]] = {}
        for i, m in enumerate(data):
            ttypes, method = m['method_used'].split()
            if i < 4:
                methods_order.append(method)
            if infos.get(ttypes) is not None:
                infos[ttypes].append(round(m['machine'].time_on_machine))
            else:
                infos[ttypes] = [round(m['machine'].time_on_machine)]

        bars = [
            go.Bar(name=key, x=methods_order, y=info)
            for key, info in infos.items()
        ]

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
            edge_x.extend((x0, x1, None))
            edge_y.extend((y0, y1, None))
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
        for adjacencies in G.adjacency():
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
        ...
        # import networkx as nx
        # import random
        # G = nx.DiGraph()
        # random.seed(10)
        # for task in tasks:
        #     G.add_node(task.get_key())
        #     for edge in task.children_edges:
        #         G.add_edge(task, edge.node)
        # pos = {t: [10, t.level] for t in tasks}
        # nx.set_node_attributes(G, pos, "pos")
        # return G

    @staticmethod
    def compare_schedule_len(data, labels):

        x = np.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots()

        rects = []
        # for key, val in data.items():
        # rect = ax.bar(x - width / 2, val, width, label=str(key))
        rects1 = ax.bar(x - width / 2, data['BEST'], width, label='Men')
        rects.append(rects1)
        # rects = [ax.bar(x - width / 2, val, width, label=str(key)) for key, val in data.items()]

        ax.set_ylabel('Scores')
        ax.set_title('Scores by group and gender')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        def __autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        for r in rects:
            __autolabel(r)

        plt.show()

    @staticmethod
    def visualize_machines(machines):
        import plotly.express as px
        import pandas as pd

        all_tasks = []
        ordered_tasks = [sorted(m.tasks, key=lambda t: t.start) for m in machines]
        for tasks in ordered_tasks:
            for task in tasks:
                slp = task.slowest_parent if task.slowest_parent is not None else {'parent_task': None, 'cummonication_time': -1}
                all_tasks.append(
                    dict(
                        TaskName=task.name,
                        TaskID=task.id,
                        SlowestParent=f"{slp['parent_task'].name if slp['parent_task'] is not None else 'None'} "
                                      f" w: {slp['communication_time']}",
                        Start=task.start, Finish=task.end, Machine=f"M-{task.machine_id}", WF_ID=task.wf_id))
                # all_tasks.append(dict(Task=task.name, Start=task.start, Finish=task.end, Machine=f"{task.machine_id} - T[{task.name}]", WF_ID=task.wf_id))

        df = pd.DataFrame(all_tasks)
        df['delta'] = df['Finish'] - df['Start']

        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Machine", hover_data=["TaskName", "SlowestParent", "TaskID"], color="WF_ID")
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
