from collections import defaultdict
import json

class Profile_parser:
    def __init__(self):
        self.timing_info = defaultdict(lambda: defaultdict(float))
        self.massif_info = defaultdict(lambda: defaultdict(float))
        self.cache_info = defaultdict(lambda: defaultdict(float))
    
    def parse(self, prof_file):
        lines = prof_file.readlines()
        for line in lines:
            line = line.strip()
            keys = line.split(':')
            sections = keys[1].split('-')

            if (len(sections) > 1):
                self.timing_info[keys[0]][sections[0]+"-total"] += float(keys[2])
                self.timing_info[keys[0]][sections[0]+"-count"] += 1
            self.timing_info[keys[0]][keys[1]] += float(keys[2])
        
        json_file = open("build/json_dump.json", "w")
        json.dump(self.timing_info, json_file)
        prof_file.close()
        json_file.close()

    def massif_parse(self, massif_file):
        lines = massif_file.readlines()
        reached = False
        count = 0
        for line in lines:
            if (reached == False):
                if (line[:19]=="Number of snapshots"):
                    reached = True
            else:
                line.strip()
                values = line.split()
                if (len(values) == 6 ) and (values[0].isdigit()):
                    if (count%5 == 0):
                        self.massif_info[int(values[0])] = {
                                                        "time": int(values[1].replace(',','')),
                                                        "total": int(values[2].replace(',','')),
                                                        "heap": int(values[3].replace(',','')),
                                                        "stack": int(values[5].replace(',',''))   
                                                        }
                    count += 1
        massif_dump = open("build/massif_dump.json", "w")
        json.dump(self.massif_info, massif_dump)
        massif_file.close()
        massif_dump.close()

    def cache_parse(self, cache_file):
        lines = cache_file.readlines()
        reached = False
        count = 0
        for line in lines:
            if (reached == False):
                if (line[:4]=="----"):
                    reached = True
            else:
                line.strip()
            
                if "PROGRAM TOTALS" in line or "???:" in line: 
                    values = line.split()
                    key = values[10] if "PROGRAM" in values[9] else values[9][4:]
                    f = lambda x: 0 if x == "." else int(x.replace(',',''))
                    self.cache_info[key] = {
                                                    "Instructions": f(values[0]),
                                                    "DataRead": f(values[1]),
                                                    "DataWrite": f(values[2]),
                                                    "InstructionMissL1": f(values[3]),
                                                    "DataReadMissL1": f(values[4]),
                                                    "DataWriteMissL1": f(values[5]),
                                                    "InstructionMissL2": f(values[6]),
                                                    "DataReadMissL2": f(values[7]),
                                                    "DataWriteMissL2": f(values[8])  
                                                    }
        cache_dump = open("build/cache_dump.json", "w")
        json.dump(self.cache_info, cache_dump)
        cache_file.close()
        cache_dump.close()