import sys, argparse, os
from mapping import *
from util import save_csv, UTTERANCE


if __name__ == "__main__":
    
    ''' 
    parser = argparse.ArgumentParser()
    parser.add_argument('-u' , dest='utterance_filename', required=True, help='Utterance file path')
    parser.add_argument('-y' , dest='predict_filename'  , required=True, help='Predicted label file path')
    parser.add_argument('-o' , dest='output_filename'   , required=True, help='Output filename')
    opts = parser.parse_args(sys.argv[1:])  
    '''
    
    sil_id = 37
    sil = 'L'

    predict_filename = sys.argv[1]
    output_filename = sys.argv[2]

    
    utterance_all = []        
    with open(predict_filename, 'r') as f:
        print "Load %s..." %predict_filename
        for line in f.readlines():
            id_list = line.rstrip().split()
            name = id_list[0]
            id_list = id_list[1:]
            utterance = UTTERANCE()
            utterance.name = name;
            utterance.phone_list = [dict_idx48_to_chr[int(id)] for id in id_list ]
            utterance_all.append(utterance)

    data = [] 
    for utterance in utterance_all:
        utterance.trimming()
        data.append([utterance.name, utterance.phone_sequence])
        
    
    header = ["id", "phone_sequence"]
    save_csv(output_filename, header, data)  
