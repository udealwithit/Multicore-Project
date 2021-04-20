import json
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self):
        json_file = open('build/json_dump.json','r')
        self.timing_info = json.load(json_file)
        json_file.close()
    
    def visualise(self):
        self.per_thread_parallel()
        self.per_thread_parallel_for()
        self.per_thread_wait_time()
        self.per_thread_critical_time()
        
    def per_thread_parallel(self):
        threads = []
        parallel_times = []
        for key in self.timing_info:
            if "parallel" in self.timing_info[key]:
                threads.append(key)
                parallel_times.append(self.timing_info[key]["parallel"])
        if (threads):
            plt.bar(threads, parallel_times)
            plt.xlabel("Thread Id")
            plt.ylabel("Time in seconds")
            plt.title("Time per thread in parallel region")
            plt.show()

    def per_thread_parallel_for(self):
        threads = []
        parallel_times = []
        for key in self.timing_info:
            if "parallelfor" in self.timing_info[key]:
                threads.append(key)
                parallel_times.append(self.timing_info[key]["parallelfor"])
        
        if (threads):
            plt.bar(threads, parallel_times)
            plt.xlabel("Thread Id")
            plt.ylabel("Time in seconds")
            plt.title("Time per thread in parallel for region")
            plt.show()
    
    def per_thread_wait_time(self):
        threads = []
        avg_wait_time = []
        for key in self.timing_info:
            for sections in self.timing_info[key]:
                section = sections.split("-")
                if (len(section) > 1) and (section[0] == "critical_wait"):
                    threads.append(key)
                    avg = self.timing_info[key]["critical_wait-total"]/self.timing_info[key]["critical_wait-count"]
                    avg_wait_time.append(avg)
        
        if (threads):
            plt.bar(threads, avg_wait_time)
            plt.xlabel("Thread Id")
            plt.ylabel("Avg Wait Time in seconds")
            plt.title("Avg Wait Time per thread in for critical region")
            plt.show()

    def per_thread_critical_time(self):
        threads = []
        avg_time = []
        for key in self.timing_info:
            for sections in self.timing_info[key]:
                section = sections.split("-")
                if (len(section) > 1) and (section[0] == "critical"):
                    threads.append(key)
                    avg = self.timing_info[key]["critical-total"]/self.timing_info[key]["critical-count"]
                    avg_time.append(avg)
        
        if (threads):
            plt.bar(threads, avg_time)
            plt.xlabel("Thread Id")
            plt.ylabel("Avg Wait Time in seconds")
            plt.title("Avg Wait Time per thread in for critical region")
            plt.show()
