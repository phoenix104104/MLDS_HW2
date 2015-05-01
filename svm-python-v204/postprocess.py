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

    utterance_filename = '../../feature/train.fbank.uname'
    predict_filename = '../../feature/train.fbank.idx_label'
    output_filename = 'test.csv'


    utterance_all = []
    with open(utterance_filename, 'r') as f:
        print "Load %s..." %utterance_filename
        for line in f.readlines():
            utterance = UTTERANCE()
            utterance.name = line.rstrip()
            utterance_all.append(utterance)
    
    predict_all = []        
    with open(predict_filename, 'r') as f:
        print "Load %s..." %predict_filename
        lines = f.readlines()
        n_line = len(lines)
        for i in range(n_line):
            utterance = utterance_all[i]
            id_list = lines[i].rstrip().split()
            utterance.phone_list = [dict_idx48_to_chr[int(id)] for id in id_list ]
    
    data = [] 
    for utterance in utterance_all:
        utterance.trimming()
        data.append([utterance.name, utterance.phone_sequence])
        
    
    header = ["id", "phone_sequence"]
    save_csv(output_filename, header, data)  





