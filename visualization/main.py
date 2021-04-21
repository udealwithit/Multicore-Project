from profile_parser import Profile_parser
from visualizer import Visualizer

prof_file = open("build/prof", "r")
parser = Profile_parser()
parser.parse(prof_file)
prof_file.close()

massif_file = None
cache_file = None

try:
    massif_file = open("build/massif_log", "r")
except:
    pass

try:
    cache_file = open("build/callgrind_log", "r")
except:
    pass

if (massif_file is not None):
    parser.massif_parse(massif_file)
    massif_file.close()

if (cache_file is not None):
    parser.cache_parse(cache_file)
    cache_file.close()

visualizer = Visualizer()
visualizer.visualise()