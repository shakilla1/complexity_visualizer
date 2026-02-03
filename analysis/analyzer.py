import time
import random
from .algorithms import bubble_sort

def run_analysis(algo, n, steps):
    data = [random.randint(0, n) for _ in range(n)]
    timings = []

    start_time = int(time.time() * 1000)

    for _ in range(steps):
        temp = data.copy()
        t1 = time.time()
        if algo == "bubble":
            bubble_sort(temp)
        t2 = time.time()
        timings.append((t2 - t1) * 1000)

    end_time = int(time.time() * 1000)

    return {
        "start_time": start_time,
        "end_time": end_time,
        "total_time_ms": end_time - start_time,
        "timings": timings
    }
