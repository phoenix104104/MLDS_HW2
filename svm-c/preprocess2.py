import os, sys
from operator import itemgetter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', action='store_true', help='add bias to feature')
parser.add_argument('-n', action='store_true', help='do normalization')
parser.add_argument('-f', dest='feature_type', required=True, help='feature type')

args = parser.parse_args()

path = '../../'
mean = var = None

def split_label_line(line) :
	s = line.rstrip().split(',')
	name = s[0].split('_')
	return ('_'.join(name[0:2]), int(name[2]), label_list.index(s[1]))

def normalize(lines) :
	feature = [[float(i) for i in line[1].split()] for line in lines]
	dim = len(feature[0])
	total = len(feature)

	global mean, var
	if mean == None or var == None :
		x = [.0] * dim
		x2 = [.0] * dim
		for f in feature :
			x = [x[i] + f[i] for i in range(dim)]
			x2 = [x2[i] + pow(f[i],2) for i in range(dim)]

		mean = [i/total for i in x]
		var = [x2[i]/total - pow(mean[i], 2) for i in range(dim)]
	
	return [[lines[i][0]] + ["%.8f" %((feature[i][j] - mean[j])/var[j]) for j in range(dim)] for i in range(total)]

label_list = []
file = open(path+'48_idx_chr.map_b')
for line in file:
	label_list.append(line.split()[0])
file.close()

file = open(path+'label/train.lab')
all_label = [split_label_line(line) for line in file]
file.close()

all_label = sorted(all_label, key=itemgetter(0,1))

if not os.path.exists(path+'feature') :
	os.makedirs(path+'feature')

for file_type in ['train', 'test'] :
	feature_type = args.feature_type
	
	ipath = path + 'ark/%s/%s.ark' %(feature_type, file_type)
	opath = path + 'feature/%s.%s' %(file_type, feature_type) + '.norm'*args.n + '.bias'*args.b

	ifile = open(ipath, 'r')
	print "Load %s" %ipath
	lines = [x.rstrip().split(None, 1) for x in ifile]
	ifile.close()

	if args.n :
		print "Normalization..."
		lines = normalize(lines)

	if args.b :
		print "Add bias..."
		lines = [line + ['1.0'] for line in lines]

	ofile = open(opath, 'w+')
	print "Save %s" %opath
	if file_type == 'train' :
		assert len(all_label) == len(lines)
		for label, line in zip(all_label, lines) :
			filename = label[0] + '_' + str(label[1])
			index = str(label[2])

			assert filename == line[0]
			line.insert(1, index)
			ofile.write(' '.join(line)+'\n')

	else :
		for line in lines :
			line.insert(1, '0')
			ofile.write(' '.join(line) + '\n')

	ofile.close()
