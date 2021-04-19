from collections import defaultdict
prof_file = open("build/prof", "r")

timing_info = defaultdict(lambda: defaultdict(float))
lines = prof_file.readlines()
for line in lines:
    line = line.strip()
    arr = line.split(':')
    timing_info[arr[0]][arr[1]] += float(arr[2])

print(timing_info)