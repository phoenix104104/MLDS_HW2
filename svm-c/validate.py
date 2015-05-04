#!/usr/bin/python
import sys
from util import load_csv

def edit_dist(a,b):
    present = range(0, len(b)+1)
    for i in range(1, len(a)+1):
        prev = present
        present = [0]
        for j in range(1, len(b)+1):
            if(a[i-1] == b[j-1]):
                present.append(prev[j-1])
            else:
                present.append(min(prev[j-1], prev[j], present[j-1])+1)
    return present[-1]

if(__name__ == '__main__'):
    if(len(sys.argv)!=3):
        print "Usage: python validate.py <ground_truth_file> <output_label_file>"
        exit()

    ground_truth = load_csv(sys.argv[1])
    label = load_csv(sys.argv[2])

    # match ground truth in output
    all_dist = 0
    for truth in ground_truth:
        idx = -1
        for i in range(0, len(label)):
            if(truth[0] == label[i][0]):
                idx = i
                break
        if(idx==-1):
            print "Entry not found: %s" %truth[0]
            break
        all_dist += edit_dist(truth[1], label[i][1])
    print "Average edit distance = %f" %(float(all_dist)/len(ground_truth))
