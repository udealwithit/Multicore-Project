from profile_parser import Profile_parser
from visualizer import Visualizer

prof_file = open("build/prof", "r")

parser = Profile_parser()
parser.parse(prof_file)
prof_file.close()

visualizer = Visualizer()
visualizer.visualise()