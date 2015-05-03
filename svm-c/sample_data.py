import numpy as np
import random, os

def extract_audio_name(string):
    s = string.split('_')
    name = s[0] + '_' + s[1]
    return name

n_sample = 400
list_dir = '../../list'
filename = os.path.join(list_dir, 'train%d.list' %n_sample)
print "Load %s" %filename
train_index = np.loadtxt(filename, dtype='int')

filename = os.path.join(list_dir, 'valid%d.list' %n_sample)
print "Load %s" %filename
valid_index = np.loadtxt(filename, dtype='int')

feature_dir = '../../feature'
fv_name = 'fbank'

feature_filename = os.path.join(feature_dir, 'train.%s' %fv_name)
train_filename = os.path.join(feature_dir, 'train%d.%s' %(n_sample, fv_name) )
valid_filename = os.path.join(feature_dir, 'valid%d.%s' %(n_sample, fv_name) )

audio_all = []
n_audio = 0
with open(feature_filename, 'r') as f:
    print "Load %s" %feature_filename
    current_name = ""
    for line in f.readlines():
        s = line.rstrip().split()
        audio_name = extract_audio_name(s[0])
        if( audio_name != current_name ):
            current_name = audio_name
            if( n_audio > 0 ):
                audio_all.append(frame_list)

            frame_list = []
            n_audio += 1

        frame_list.append(line)
    
    audio_all.append(frame_list)
    
audio_train = []
for index in train_index:
    audio_train.append(audio_all[index])

audio_valid = []
for index in valid_index:
    audio_valid.append(audio_all[index])

with open(train_filename, 'w') as f:
    print "Save %s" %train_filename
    for audio in audio_train:
        for frame in audio:
            f.write(frame)

with open(valid_filename, 'w') as f:
    print "Save %s" %valid_filename
    for audio in audio_valid:
        for frame in audio:
            f.write(frame)

