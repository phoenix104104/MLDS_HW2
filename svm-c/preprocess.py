import os, sys
from operator import itemgetter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', action='store_true', help='add 1 to feature')
parser.add_argument('-n', action='store_true', help='do normalization')
parser.add_argument('-mfcc', action='store_true', help='create mfcc feature')

args = parser.parse_args()

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

def normalize(lines) :
	feature = [[float(i) for i in line[1].split()] for line in lines]

	dim = len(feature[0])
	x = [.0] * dim
	x2 = [.0] * dim
	for f in feature :
		x = [x[i] + f[i] for i in range(dim)]
		x2 = [x2[i] + pow(f[i],2) for i in range(dim)]

	total = len(feature)
	mean = [i/total for i in x]
	var = [x2[i]/total - pow(mean[i], 2) for i in range(dim)]
	
	return [[lines[i][0]] + [str((feature[i][j] - mean[j])/var[j]) for j in range(dim)] for i in range(total)]


all_label = sorted(all_label, key=itemgetter(0,1))

if not os.path.exists(path+'feature') :
	os.makedirs(path+'feature')

# train
for feature_type in ['fbank3_512']:
	
	ipath = path+'%s/train.ark' %feature_type
	opath = path+'feature/train.%s' %feature_type + '.norm'*args.n + '.add'*args.a
#	if os.path.exists(opath) :
#		print 'skip file %s, already exists' %opath
#		continue

	print "Load %s" %ipath
	ifile = open(ipath)
	ofile = open(opath, 'w+')

	lines = [x.rstrip().split(None, 1) for x in ifile]
	if args.n :
		lines = normalize(lines)

	if args.a :
		lines = [line + ['1.0'] for line in lines]

	assert len(all_label) == len(lines)
	for label, line in zip(all_label, lines) :
		filename = label[0] + '_' + str(label[1])
		index = str(label[2])

		assert filename == line[0]
		line.insert(1, index)
		ofile.write(' '.join(line)+'\n')

	print "Save %s" %opath

# test
for feature_type in ['fbank3_512']:
	
	ipath = path+'%s/test.ark' %feature_type
	opath = path+'feature/test.%s' %feature_type + '.norm'*args.n + '.add'*args.a
	if os.path.exists(opath) :
		print 'skip file %s, already exists' %opath
		continue

	print "Load %s" %ipath
	ifile = open(ipath)
	ofile = open(opath, 'w+')

	lines = [x.rstrip().split(None, 1) for x in ifile]

	if args.n :
		lines = normalize(lines)

	if args.a :
		lines = [line + ['1.0'] for line in lines]

	for line in lines :
		line.insert(1, '0')
		ofile.write(' '.join(line) + '\n')

	print "Save %s" %opath
