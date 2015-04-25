import os
from operator import itemgetter

path = '../../'

label_list = []
file = open(path+'48_idx_chr.map_b')
for line in file:
	label_list.append(line.split()[0])
file.close()

def split_label_line(line) :
	s = line.rstrip().split(',')
	name = s[0].split('_')
	return ('_'.join(name[0:2]), int(name[2]), label_list.index(s[1]))

file = open(path+'label/train.lab')
all_label = [split_label_line(line) for line in file]
file.close()

all_label = sorted(all_label, key=itemgetter(0,1))

f_fbank = open(path+'fbank/train.ark')
f_mfcc = open(path+'mfcc/train.ark')

if not os.path.exists(path+'feature') :
	os.makedirs(path+'feature')

o_fbank = open(path+'feature/train.fbank', 'w+')
o_mfcc = open(path+'feature/train.mfcc', 'w+')

for label in all_label :
	filename = label[0] + '_' + str(label[1])
	index = str(label[2])

	line = f_fbank.readline().split(None, 1)
	assert filename == line[0]
	line.insert(1, index)
	o_fbank.write(' '.join(line))

	line = f_mfcc.readline().split(None, 1)
	assert filename == line[0]
	line.insert(1, index)
	o_mfcc.write(' '.join(line))