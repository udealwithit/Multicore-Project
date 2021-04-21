import json
import matplotlib.pyplot as plt
import pandas as pd
import os

class Visualizer:
    def __init__(self):
        json_file = open('build/json_dump.json','r')
        self.timing_info = json.load(json_file)
        json_file.close()

        self.massif_info = None
        self.cache_info = None
        
        try:
            with open('build/massif_dump.json','r') as massif_file:
                self.massif_info = json.load(massif_file)
        except:
            pass

        try:
            with open('build/cache_dump.json','r') as cache_file:
                self.cache_info = json.load(cache_file)
        except:
            pass

    def visualise(self,sections):
        for section in sections:
            self.per_thread(section)
        # self.per_thread_parallel()
        # self.per_thread_parallel_for()
        # self.per_thread_atomic()
        self.per_thread_wait_time()
        self.per_thread_critical_time()
        
        if self.cache_info is not None:
            self.cache_visualise()
        
        if self.massif_info is not None:
            self.massif_visualise()

    def per_thread(self,section):
        threads = []
        parallel_times = []
        thread_counts = []
        checkForZero = True
        for key in self.timing_info:
            if section in self.timing_info[key]:
                threads.append(key)
                if self.timing_info[key][section] != 0:
                    checkForZero = False
                thread_counts.append(self.timing_info[key][section+"_tcount"])
                parallel_times.append(self.timing_info[key][section])
        if (threads):
            fig,ax = plt.subplots()
            if checkForZero:
                ax.bar(threads, thread_counts)
                ax.set_ylabel("Number of times thread executed")
                ax.set_title("Execution count per thread in " + section + " region")
            else:
                ax.bar(threads, parallel_times)
                ax.set_ylabel("Time in seconds")
                ax.set_title("Time per thread in " + section + " region")
            ax.set_xlabel("Thread Id")
            fig.savefig("output/per_thread_"+section+".png")
    
    # def per_thread_parallel(self):
    #     threads = []
    #     parallel_times = []
    #     for key in self.timing_info:
    #         if "parallel" in self.timing_info[key]:
    #             threads.append(key)
    #             parallel_times.append(self.timing_info[key]["parallel"])
    #     if (threads):
    #         plt.bar(threads, parallel_times)
    #         plt.xlabel("Thread Id")
    #         plt.ylabel("Time in seconds")
    #         plt.title("Time per thread in parallel region")
    #         plt.savefig("output/per_thread_parallel.png")

    # def per_thread_parallel_for(self):
    #     threads = []
    #     parallel_times = []
    #     for key in self.timing_info:
    #         if "parallelfor" in self.timing_info[key]:
    #             threads.append(key)
    #             parallel_times.append(self.timing_info[key]["parallelfor"])
        
    #     if (threads):
    #         plt.bar(threads, parallel_times)
    #         plt.xlabel("Thread Id")
    #         plt.ylabel("Time in seconds")
    #         plt.title("Time per thread in parallel for region")
    #         plt.savefig("output/per_thread_parallel_for.png")
    
    # def per_thread_atomic(self):
    #     threads = []
    #     parallel_times = []
    #     for key in self.timing_info:
    #         if "atomic" in self.timing_info[key]:
    #             threads.append(key)
    #             parallel_times.append(self.timing_info[key]["atomic"])
    #     if (threads):
    #         plt.bar(threads, parallel_times)
    #         plt.xlabel("Thread Id")
    #         plt.ylabel("Time in seconds")
    #         plt.title("Time per thread in atomic region")
    #         plt.savefig("output/per_thread_atomic.png")
    
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
            plt.savefig("output/per_thread_wait_time.png")

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
            plt.savefig("output/per_thread_critical_time.png")

    def massif_visualise(self):
        time = []
        total_mem = []
        heap_mem = []
        stack_mem = []

        for key in self.massif_info:
            time.append(self.massif_info[key]['time'])
            total_mem.append(self.massif_info[key]['total']/float(1024))
            heap_mem.append(self.massif_info[key]['heap']/float(1024))
            stack_mem.append(self.massif_info[key]['stack']/float(1024))

        fig,axs = plt.subplots(2,2)
        
        axs[0][0].plot(time,total_mem,label="Total Memory Usage")
        axs[0][0].set_xlabel('Time in ms')
        axs[0][0].set_ylabel('Memory in KB')
        
        axs[0][1].plot(time,heap_mem,label="Heap Usage")
        axs[0][1].set_xlabel('Time in ms')
        axs[0][1].set_ylabel('Memory in KB')
        
        axs[1][0].plot(time,stack_mem,label="Stack Usage")
        axs[1][0].set_xlabel('Time in ms')
        axs[1][0].set_ylabel('Memory in KB')
        
        # plt.legend()
        fig.savefig("output/massif_visualise.png")

    def cache_visualise(self):
        data = []
        columns = ["Function_Name"]
        populate_columns = False
        for key in self.cache_info:
            val = [key]
            for key2 in self.cache_info[key]:
                if (not populate_columns):
                    columns.append(key2)
                val.append(self.cache_info[key][key2])
            data.append(val)
            if (not populate_columns):        
                populate_columns = True
        
        dataframe = pd.DataFrame(data,columns=columns)
        fig, ax = plt.subplots() 
        ax.axis('off')
        ax.axis('tight')

        the_table = ax.table(cellText=dataframe.values, colLabels=dataframe.columns, loc='center')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(5)
        fig.tight_layout()
        fig.savefig("output/cache_visualise.png")
