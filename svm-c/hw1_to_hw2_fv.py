from util import load_hw1_feature, save_hw2_feature
import os, sys
import numpy as np

#input_dir = '../../hw1_feature'
input_dir = '../../../hw1/feature'
output_dir = '../../feature'

fv_name = sys.argv[1]#'fbank4.norm.nn2048_2048_48.L3.norm'

map_filename = '../../48_idx_chr.map_b'
with open(map_filename, 'r') as f:
    print "Load %s" %map_filename
    map = [line.split()[0] for line in f.readlines()]



for t in ["train", 'test', 'test.old']:
    filename = os.path.join(input_dir, "%s.%s"%(t, fv_name))
    X = load_hw1_feature(filename)
    
    (N, D) = X.shape
    B = np.ones((N, 1))
    X = np.append(X, B, axis=1) # add bias term

    filename = '../../frame/%s.frame' %t
    with open(filename, 'r') as f:
        print "Load %s" %filename
        frame = [line.rstrip() for line in f.readlines()]

    output_filename = os.path.join(output_dir, '%s.%s'%(t, fv_name) )
    
    if( t == "train" ):
        filename = '../../label/%s.label' %t
        with open(filename, 'r') as f:
            label = [line.rstrip() for line in f.readlines()]
        
        save_hw2_feature(output_filename, X, frame, label)

    else:
        
        save_hw2_feature(output_filename, X, frame)



