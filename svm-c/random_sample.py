import numpy as np
import random, os

N = 462
train_num = 400
valid_num = 62

sample_index = random.sample(range(N), train_num + valid_num)
train_index = sorted(sample_index[:train_num])
valid_index = sorted(sample_index[train_num:])

output_dir = '.'
filename = os.path.join(output_dir, 'train%d.list' %train_num)
print "Save %s" %filename
np.savetxt(filename, train_index, fmt='%d')

filename = os.path.join(output_dir, 'valid%d.list' %train_num)
print "Save %s" %filename
np.savetxt(filename, valid_index, fmt='%d')

