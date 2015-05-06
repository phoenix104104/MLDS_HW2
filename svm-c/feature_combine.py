import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True, nargs='+', dest='inputs', help='file to combine (specify train file and test file will combine automatically)')
parser.add_argument('-o', required=True, dest='output', help='output file, should contain "train" in filename to generate corresponding test file')
args = parser.parse_args()

assert len(args.inputs) >= 2
assert all(['train' in x for x in args.inputs])
inputfiles = [[open(x) for x in args.inputs], [open(x.replace('train', 'test')) for x in args.inputs]]

assert 'train' in args.output
outputfiles = [open(args.output, 'w+'), open(args.output.replace('train', 'test'), 'w+')]

for i in range(2) :
	while True :
		lines = [f.readline().rstrip().split(None,2) for f in inputfiles[i]]
		if len([x for line in lines for x in line]) == 0 :
			break

		header = list(set([' '.join(line[:2]) for line in lines]))
		assert len(header) == 1
		outputfiles[i].write(' '.join(header+[line[2] for line in lines])+'\n')
