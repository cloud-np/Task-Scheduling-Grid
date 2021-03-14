import matplotlib
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

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')



