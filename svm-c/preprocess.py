import os, sys
from operator import itemgetter
import argparse

sep = os.path.sep
path = '..%s..%s' %(sep, sep)

parser = argparse.ArgumentParser()
parser.add_argument('-a', action='store_true', help='add 1 to feature')
parser.add_argument('-n', action='store_true', help='do normalization')
parser.add_argument('-f', dest='feature_folder', type=str, help='feature folder, should contain train.ark and test.ark, default %sfbank' %path)
parser.add_argument('-o', dest='output_path', help='output path, default %sfeature' %path)
parser.add_argument('-tag', dest='output_file_tag', help='tag appends to output filename')

args = parser.parse_args()

folder = path+'fbank'+sep if args.feature_folder == None else args.feature_folder
output_path = path+'feature'+sep if args.output_path == None else args.output_path 
tag = '' if args.output_file_tag == None else args.output_file_tag

mean = var = None

def split_label_line(line) :
	s = line.rstrip().split(',')
	name = s[0].split('_')
	return ('_'.join(name[0:2]), int(name[2]), label_list.index(s[1]))

def normalize(ifile, flag) :
	global mean, var

	ifile.seek(0)
	line = ifile.readline().split()[1:]
	dim = len(line)

	if not flag :
		mean = [.0] * dim
		var = [1.0] * dim
		return

	if mean == None or var == None :
		x = [float(i) for i in line]
		x2 = [pow(float(i), 2) for i in line]

		count = 1
		for line in ifile :
			line = [float(i) for i in line.split()[1:]]
			x = [x[i] + line[i] for i in range(dim)]
			x2 = [x2[i] + pow(line[i],2) for i in range(dim)]

			count += 1

		mean = [i/count for i in x]
		var = [x2[i]/count - pow(mean[i], 2) for i in range(dim)]
	return

def split_line(line, nflag, aflag) :
	if nflag :
		global mean, var
		line = line.split()
		feature = [str((float(line[i])-mean[i])/var[i]) for i in range(len(mean))]
	else :
		feature = [line]
	if aflag :
		feature.append('1.0')
	return feature

label_list = []
file = open(path+'48_idx_chr.map_b')
for line in file:
	label_list.append(line.split()[0])
file.close()

file = open(path+'label%strain.lab' %sep)
all_label = [split_label_line(line) for line in file]
file.close()

all_label = sorted(all_label, key=itemgetter(0,1))

if not os.path.exists(output_path) :
	os.makedirs(output_path)

for file_type in ['train', 'test'] :
	ipath = os.path.join(folder, '%s.ark' %file_type)
	opath = os.path.join(output_path, '%s.%s' %(file_type, folder.rstrip(sep).split(sep)[-1])) + '.norm'*args.n + '.add'*args.a
	if os.path.exists(opath) :
		print 'skip file %s, already exists' %opath
		continue

	ifile = open(ipath)
	ofile = open(opath, 'w+')

	normalize(ifile, args.n)

	ifile.seek(0)
	if file_type == 'train' :
		for label, line in zip(all_label, ifile) :
			filename = label[0] + '_' + str(label[1])
			index = str(label[2])

			line = line.rstrip().split(None, 1)
			assert filename == line[0]

			feature = split_line(line[1], args.n, args.a)

			ofile.write(' '.join([filename] + [index] + feature)+'\n')

	else :
		for line in ifile :
			line = line.rstrip().split(None, 1)

			feature = split_line(line[1], args.n, args.a)

			ofile.write(' '.join([line[0]] + ['0'] + feature) + '\n')

	print 'Save as %s' %opath
