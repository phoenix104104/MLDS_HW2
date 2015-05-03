import numpy as np
import random, os

N = 3696
train_num = 400
valid_num = 400

sample_index = random.sample(range(N), train_num + valid_num)
train_index = sample_index[:train_num]
valid_index = sample_index[train_num+1:]

output_dir = '../../list'
filename = os.path.join(output_dir, 'train400.list')
print "Save %s" %filename
np.savetxt(filename, train_index, fmt='%d')

filename = os.path.join(output_dir, 'valid400.list')
print "Save %s" %filename
np.savetxt(filename, valid_index, fmt='%d')

