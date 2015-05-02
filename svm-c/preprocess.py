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

if not os.path.exists(path+'feature') :
	os.makedirs(path+'feature')

for feature_type in ['fbank', 'mfcc'] :
	
	ipath = path+'%s/train.ark' %feature_type
	opath = path+'feature/train.%s' %feature_type
	if os.path.exists(opath) :
		print 'skip file %s, already exists' %opath
		continue

	ifile = open(ipath)
	ofile = open(opath, 'w+')

	for label in all_label :
		filename = label[0] + '_' + str(label[1])
		index = str(label[2])

		line = ifile.readline().split(None, 1)
		assert filename == line[0]
		line.insert(1, index)
		ofile.write(' '.join(line))


for feature_type in ['fbank', 'mfcc'] :
	
	ipath = path+'%s/test.ark' %feature_type
	opath = path+'feature/test.%s' %feature_type
	if os.path.exists(opath) :
		print 'skip file %s, already exists' %opath
		continue

	ifile = open(ipath)
	ofile = open(opath, 'w+')

	for line in ifile :
		s = line.split(None, 1)
		s.insert(1, '0')
		ofile.write(' '.join(s))

