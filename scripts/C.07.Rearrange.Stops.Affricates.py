import os, shutil, sys

sys_name = sys.argv[1]
contexts = ["affricates_CV", "affricates_VC", "affricates_isolate", "stops_CV", "stops_VC", "stops_isolate"]
source_folder = "../data/" + sys_name + "/06.context_separation_consonants/"

for cont in contexts:
	to_be_rearranged = source_folder + cont	
	fil_to_move = [fil for fil in os.listdir(to_be_rearranged) if os.path.isfile(to_be_rearranged + '/' + fil) == True]
	for fil in fil_to_move:
		shutil.move(to_be_rearranged + '/' + fil, to_be_rearranged + '/stops_with_closure/' + fil)