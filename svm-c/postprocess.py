#!/usr/bin/python -u
import sys, argparse, os
from mapping import *
from util import save_csv, UTTERANCE


if __name__ == "__main__":
    
     
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' , dest='predict_filename'  , required=True, help='Predicted label file path')
    parser.add_argument('-o' , dest='output_filename'                  , help='Output filename')
    opts = parser.parse_args(sys.argv[1:])  
    
    
    sil_id = 37
    sil = 'L'

    #predict_filename = '../../feature/train.fbank.label'
    #output_filename = 'train_output.csv'
    predict_filename = opts.predict_filename
    if( opts.output_filename ):
        output_filename = opts.output_filename
    else:
        output_filename = predict_filename + '.csv'
    
    utterance_all = []        
    with open(predict_filename, 'r') as f:
        print "Load %s..." %predict_filename
        for line in f.readlines():
            id_list = line.rstrip().split()
            name = id_list[0]
            id_list = id_list[1:]
            utterance = UTTERANCE()
            utterance.name = name
            utterance.phone_list = [dict_idx48_to_chr[int(id)] for id in id_list ]
            utterance_all.append(utterance)

    data = [] 
    current_name = ''
    seq_dict = dict()
    for utterance in utterance_all:
        utterance.trimming()
        if(utterance.name != current_name):
            current_name = utterance.name
            seq_dict.clear()
        if(seq_dict.get(utterance.phone_sequence, 0) == 0):
            data.append([utterance.name, utterance.phone_sequence])
            seq_dict[utterance.phone_sequence] = 1
    
    header = ["id", "phone_sequence"]
    save_csv(output_filename, header, data)  





