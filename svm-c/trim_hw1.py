#!/usr/bin/python
import csv
from mapping import *
import os, argparse, sys
from util import load_csv, save_csv, UTTERANCE

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i' , dest='input_filename'  , required=True, help='Input file path')
    parser.add_argument('-o' , dest='output_filename' , help='Output filename')
    opts = parser.parse_args(sys.argv[1:])

    input_filename = opts.input_filename
    if( opts.output_filename ):
        output_filename = opts.output_filename
    else:
        basename = os.path.basename(input_filename)
        output_filename = os.path.join('../../pred', basename)


    data_all = load_csv(input_filename)
    
    current_name = ""
    utterance_all = []
    for data in data_all:
        names = data[0].split('_')
        name = names[0] + '_' + names[1]
        p39 = data[1]
        if( name != current_name ):
            current_name = name
            utterance = UTTERANCE()
            utterance.name = name
            utterance_all.append(utterance)

        utterance.phone_list.append(dict_39_to_chr[p39])
    
    data = []
    for utterance in utterance_all:
        utterance.trimming()
        data.append([utterance.name, utterance.phone_sequence])

    header = ["id", "phone_sequence"]
    save_csv(output_filename, header, data)  
