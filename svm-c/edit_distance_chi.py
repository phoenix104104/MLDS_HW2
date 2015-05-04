# 2015 0504 ymchiQQ

import sys,difflib,os
from io import open

def print_cost_matrix(len_pr,len_gt,cost_matrix):
	for j in range(len_pr+1):
		for i in range(len_gt+1):
			print cost_matrix[j][i],
		print '\n'
	#os.system('pause')
	return None


def get_ed(pr, gt):
	len_pr = len(pr)
	len_gt = len(gt)
	#print len_pr
	#print len_gt
	#os.system('pause')
	#cost_matrix[len_pr][len_gt]
	cost_matrix = [[0 for x in range(len_gt+1)] for x in range(len_pr+1)] 
	for i in range(len_pr+1):
		cost_matrix[i][0]=i
	for i in range(len_gt+1):
		cost_matrix[0][i]=i
	for j in range(len_pr):
		for i in range(len_gt):
			'''
			print j,
			print pr[j]
			print i,
			print gt[i]
			'''
			#os.system('pause')
			if pr[j] == gt[i]:
				#print 'hit'
				cost_matrix[j+1][i+1] = cost_matrix[j][i];
				#print_cost_matrix(len_pr,len_gt,cost_matrix)
			else:
				'''
				print 'nohit'
				print 'j,i+1',
				print cost_matrix[j][i+1]
				print 'j+1,i',
				print cost_matrix[j+1][i]
				print 'j,i',
				print cost_matrix[j][i]
				print 'min',
				print min(cost_matrix[j][i+1],cost_matrix[j+1][i],cost_matrix[j][i])
				'''
				cost_matrix[j+1][i+1] = 1 + min(cost_matrix[j][i+1],cost_matrix[j+1][i],cost_matrix[j][i])
				#print cost_matrix[j+1][i+1]
				#print_cost_matrix(len_pr,len_gt,cost_matrix)
			#os.system('pause')
	#print len_gt
	#print len_pr
	#print cost_matrix[len_pr][len_gt]
	#print cost_matrix[len_gt][len_pr]
	
	ed = cost_matrix[len_pr][len_gt]
	return ed


predict_result = sys.argv[1];
ground_turth = sys.argv[2];

# open json file
fp_pr = open(predict_result,'r',encoding = 'UTF-8')

# read file for Edit distance
count = 0
sum_ed = 0.0
line_pr = fp_pr.readline()

for line_pr in fp_pr:
	temp_pr = line_pr.split(',')
	#print temp_pr
	data_prid = temp_pr[0]
	data_pr = temp_pr[1]
	fp_gt = open(ground_turth,'r',encoding = 'UTF-8')
	line_gt = fp_gt.readline()
	for line_gt in fp_gt:
		#print line_pr
		#os.system('pause')
		temp_gt = line_gt.split(',')
		#print temp_gt
		data_gtid = temp_gt[0]
		data_gt = temp_gt[1]
		#print data_gt
		#print data_prid
		#print data_gtid
		#os.system('pause')
		if data_prid == data_gtid:
			ed = get_ed(data_pr, data_gt)
			#print ed
			sum_ed +=ed
			count +=1
			break
		#print 'sum ed is: ',
		#print ed
print 'avg ed is: ',
#print sum_ed
print sum_ed/count
#os.system('pause')

