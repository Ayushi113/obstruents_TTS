import os, shutil, sys
### remove FRICATIVES when you don't need them!!!!
context_folders = ["affricates_CV", "affricates_VC", "affricates_isolate", "stops_CV", "stops_VC", "stops_isolate"]

sys_name = sys.argv[1]

systems = [sys_name]

for sys_name in systems:
    source_stops = "../data/" + sys_name + "/04.noise_region_stops/"
    print(sys_name)
    print(os.listdir(source_stops)[0:10])
    #print(os.listdir(source_stops))
    for context in context_folders:
        context_ref = "../data/" + sys_name + "/06.context_separation_consonants/" + context + "/stops_with_closure/"
        context_dest = "../data/" + sys_name + "/06.context_separation_consonants/" + context + "/noise_region_stops/"
        ####### remove this part later - only for tgt_noise
        if os.path.exists(context_dest):
           shutil.rmtree(context_dest)

        os.mkdir(context_dest)
        print(os.listdir(context_ref)[0:10])
       ##################

        stops_to_move = [fil for fil in os.listdir(source_stops) if fil.replace("_noise.TextGrid", ".TextGrid") in os.listdir(context_ref)]
        print(stops_to_move)

        for fil in stops_to_move:
            fil_with_source = source_stops + fil
            print(fil_with_source)
            print(os.path.isfile(fil_with_source))
            shutil.copy(fil_with_source, context_dest)
        print(context)
        #print(stops_to_move)
        
#        exit(0)


