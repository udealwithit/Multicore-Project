import json
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self):
        json_file = open('build/json_dump.json','r')
        self.timing_info = json.load(json_file)
        json_file.close()
    
    def visualise(self):
        self.per_thread_parallel()

    def per_thread_parallel(self):
        threads = []
        parallel_times = []
        for key in self.timing_info:
            if "parallel" in self.timing_info[key]:
                threads.append(key)
                parallel_times.append(self.timing_info[key]["parallel"])
        
        plt.bar(threads, parallel_times)
        plt.xlabel("Thread Id")
        plt.ylabel("Time in seconds")
        plt.title("Time per thread in parallel region")
        plt.show()