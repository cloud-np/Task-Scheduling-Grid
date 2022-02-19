import numpy as np
import math

# SET V  {20, 40, 60, 80, 100}
# SET CCR  {0.1, 0.5, 1, 5, 10}
# SET  {0.5, 1.0, 2.0}
# SET out degree  {1, 2, 3, 4, 5}
# SET  {1, 0.25, 0.5, 0.75, 1}


class HeftGenerator:

    def __init__(self, n_tasks, out_degree, a, ccr, b):
        self.n_tasks = n_tasks
        mean_value = (math.sqrt(n_tasks) / a)
        self.height = math.floor(np.random.uniform(low=1, high=mean_value, size=n_tasks)[0])
        self.a = a
        self.out_degree = out_degree
        self.ccr = ccr
        self.b = b
        print(self.height)
        # print(self.height.mean())
        print(mean_value)


if __name__ == "__main__":
    HeftGenerator(n_tasks=10, out_degree=2, a=1, ccr=0.5, b=0.5)
