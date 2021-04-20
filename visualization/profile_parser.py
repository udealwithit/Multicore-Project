from collections import defaultdict
import json

class Profile_parser:
    def __init__(self):
        self.timing_info = defaultdict(lambda: defaultdict(float))
    
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