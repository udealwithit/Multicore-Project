import sys
from profile_parser import Profile_parser
from visualizer import Visualizer

prof_file = open("build/prof", "r")
parser = Profile_parser()
sections = parser.parse(prof_file)
prof_file.close()

massif_file = None
cache_files = []

try:
    massif_file = open("build/massif_log", "r")
except:
    pass

try:
    for i in range(1, len(sys.argv)):
        cache_files.append(open("build/"+sys.argv[i], "r"))
except:
    pass

if (massif_file is not None):
    parser.massif_parse(massif_file)
    massif_file.close()

if (cache_files):
    parser.cache_parse(cache_files)

visualizer = Visualizer()
visualizer.visualise(sections,len(cache_files))