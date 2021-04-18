prof_file = open("build/prof", "r")

timing_info = {}

lines = prof_file.readlines()
for line in lines:
    line = line.strip()
    arr = line.split(':')
    if (timing_info.get(arr[0], None) is None):
        timing_info[arr[0]] = {}
        timing_info[arr[0]][arr[1]] = float(arr[2])
    else:
        timing_info[arr[0]][arr[1]] += float(arr[2])

print(timing_info)