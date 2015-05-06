import numpy as np
import random, os
from util import extract_audio_name




if __name__ == '__main__':
    
    feature_dir = '../../feature'
    fv_name = 'fbank3_512.norm.bias'


    feature_filename = os.path.join(feature_dir, 'train.%s' %fv_name)
    
    n_sample = 400
    filename = 'train%d.list' %n_sample
    print "Load %s" %filename
    train_index = np.loadtxt(filename, dtype='int')
    
    filename = 'valid%d.list' %n_sample
    print "Load %s" %filename
    valid_index = np.loadtxt(filename, dtype='int')
    
    # output filename
    train_filename = os.path.join(feature_dir, 'train%d.%s' %(n_sample, fv_name) )
    valid_filename = os.path.join(feature_dir, 'valid%d.%s' %(n_sample, fv_name) )
    
    n_person = 0
    n_audio = 0
    person_all = []
    with open(feature_filename, 'r') as f:
        print "Load %s" %feature_filename
        current_person = ""
        current_audio = ""
        for line in f.readlines():
            s = line.rstrip().split()
            person, audio = extract_audio_name(s[0])
            if( person != current_person ):
                #print "person = %s, n_audio = %d" %(person, n_audio)
                current_person = person
                
                if( n_person > 0 ):
                    person_all.append(audio_list)

                audio_list = []
                n_person += 1
                n_audio = 0
                
            
            if( audio != current_audio ):
                current_audio = audio
                n_audio += 1
    
            audio_list.append(line)
        
        person_all.append(audio_list)
        
    print "Total person = %d" %len(person_all)

    person_train = []
    for index in train_index:
        person_train.append(person_all[index])
    
    person_valid = []
    for index in valid_index:
        person_valid.append(person_all[index])
    
    with open(train_filename, 'w') as f:
        print "Save %s" %train_filename
        for person in person_train:
            for line in person:
                f.write(line)
    
    with open(valid_filename, 'w') as f:
        print "Save %s" %valid_filename
        for person in person_valid:
            for line in person:
                f.write(line)
