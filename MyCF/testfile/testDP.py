#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

def drawPicture(rating_matrix, result, hasColor=True):
	'''
	绘制结果矩阵散点图
	'''
	userNum, itemNum = rating_matrix.shape
	print userNum, itemNum
	print len(result)
	user_result = {}	#存储user聚类信息
	item_result = {}	#存储item聚类信息
	for i in xrange(len(result)):
		if i < userNum:
			if user_result.has_key(result[i]):
				user_result[result[i]].append(i)
			else:
				user_result[result[i]] = [i]
		else:
			if item_result.has_key(result[i]):
				item_result[result[i]].append(i-userNum)
			else:
				item_result[result[i]] = [i-userNum]

	#draw all samples
	plt.xlim(0, userNum+1)
	plt.ylim(0, itemNum+1)
	color = [['black', 'pink'], 
	['red', 'pink'], 
	['green', 'pink'],
	['blue', 'pink'],
	['magenta', 'pink']]
	clen = len(color)
	x = 0
	colorIndex = 0
	print "Drawing the picture, but it will cost lots of time, please wait for a while......"
	for key1 in user_result.keys():
		for item1 in user_result[key1]:
			x += 1
			itemValues = rating_matrix[item1]
			y = 0
			for key2 in item_result.keys():
				for item2 in item_result[key2]:
					y += 1
					if int(itemValues[item2])!=0:
						if hasColor:
							if int(itemValues[item2])>3.5:
								plt.scatter(x, y, marker = '.', s = 3, color = color[colorIndex%clen][0])
							else:
								plt.scatter(x, y, marker = '.', s = 3, color = color[colorIndex%clen][1])
								#continue
						else:
							plt.scatter(x, y, marker = '.', s = 3, color = color[0])
		colorIndex += 1
	print "Maybe it's time to show your picture!"
	plt.show()

if __name__ == '__main__':
	src_path = os.path.join(os.getcwd(), 'datatest_3.csv')
	init_data = pd.read_csv(src_path, header = 0, index_col = 0)
	# Cause the type of columns that read in csv is str, we need to convert it into int
	int_col = [int(col) for col in init_data.columns]
	print int_col
	init_data.columns = int_col
	init_data_matrix = init_data.fillna(0).values
	result = [0]*(len(init_data.columns)+len(init_data.index))
	drawPicture(init_data_matrix, result)