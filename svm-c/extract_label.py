#!/usr/bin/python
import csv
from mapping import *
import os, argparse, sys
from util import load_csv, save_csv, UTTERANCE, extract_audio_name

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i' , dest='input_filename'  , required=True, help='Input feature file path')
    parser.add_argument('-o' , dest='output_filename' , required=True, help='Output csv filename')
    opts = parser.parse_args(sys.argv[1:])

    input_filename = opts.input_filename
    output_filename = opts.output_filename

    with open(input_filename, 'r') as f:
        print "Load %s" %input_filename
        data_all = f.readlines()
    
    current_name = ""
    utterance_all = []
    for data in data_all:
        data = data.rstrip().split()
        names = data[0].split('_')
        name = names[0] + '_' + names[1]
        idx = int(data[1])
        if( name != current_name ):
            current_name = name
            utterance = UTTERANCE()
            utterance.name = name
            utterance_all.append(utterance)

        utterance.phone_list.append(dict_idx48_to_chr[idx])
    
    data = []
    for utterance in utterance_all:
        utterance.trimming()
        data.append([utterance.name, utterance.phone_sequence])

    header = ["id", "phone_sequence"]
    save_csv(output_filename, header, data)  
