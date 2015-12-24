#coding=utf-8
#MSC means Multiple Spectral Clustering 
import numpy as np
import pandas as pd
import networkx as nx
import os, csv
import scipy.cluster.vq as scv
import scipy.cluster.hierarchy as sch
import spectral as spe
import datetime, time, copy
import matplotlib.pyplot as plt

#读取MovieLens的数据
path = os.path.join(os.getcwd(),"src/smallratings.csv")
ratings = pd.read_csv(path, header=0)

def movieCount(ratings, column):
	'''
	读取ratings数据，找出每个movie对应的评分数量（即每个movie被多少人评分）
	'''
	movieDict = {}
	for i in ratings[column]:
		if not movieDict.has_key(i):
			movieDict[i] = 1
		else:
			movieDict[i] += 1
	return movieDict

def findHotMovie(movieDict, numLimit):
	'''
	找出最热门的几个电影，numLimit为规定热门电影的阀值
	'''
	#tempList = sorted(movieDict.items(), lambda x, y: cmp(x[1], y[1]), reverse = True)	#为电影排序，找出热门电影
	hotMovieList = []
	for i in movieDict.keys():
		if movieDict[i] >= numLimit or movieDict[i] <= 2:
			hotMovieList.append(i)
	return hotMovieList

def key2value(ratings, column, hotMovieList = []):
	'''
	由于movieid/userid比较稀疏，不利于建立矩阵，所以先将movieid/userid映射到字典，不同movieid/userid对应不同value值
	'''
	keys = set(ratings[column])-set(hotMovieList)
	print "there are %d "%len(keys)+column+"s"
	keys = tuple(keys)
	values = tuple([i for i in xrange(1, len(keys)+1)])
	this_dict = {}
	#建立映射
	this_dict = dict(zip(keys, values))
	return this_dict

def getRatingarray(value_ratings, movieid_dict, userid_dict):
	'''
	根据每个用户对电影的评分数据构建user-item矩阵
	'''
	temp_l = []
	e_row = []
	user_id = 0
	flag = False
	for item in value_ratings:
		if not movieid_dict.has_key(item[1]):	#如果是热门电影
			continue
		if flag:
			temp_l.append(e_row)
		if user_id != int(item[0]):
			user_id = int(item[0])
			e_row = [0]*len(movieid_dict)
			flag = True
		else:
			flag = False
		e_row[movieid_dict[item[1]]-1] = item[2]
	rating_array = np.array(temp_l)
	print rating_array, "rating_array is get!"
	return rating_array

def code(str):
	'''
	打印出中文的话需要转码，将utf-8转换成gbk
	'''
	str2 = str.decode("utf-8").encode("gbk")
	return str2

def getEarray(rating_array, movieid_dict, userid_dict):
	'''
	构建二部图邻接矩阵E
	E = [[0 A],
		[transpose(A) 0]],
	其中A为二部图的N×M矩阵，N为总user数量，M为总电影数量
	'''
	l_len, m_len = rating_array.shape
	#m_len = len(movieid_dict)
	#l_len = len(userid_dict)
	u_l_array = np.zeros((l_len, l_len))
	u_r_array = rating_array
	d_l_array = rating_array.transpose()
	d_r_array = np.zeros((m_len, m_len))
	print u_l_array.shape, u_r_array.shape, d_l_array.shape, d_r_array.shape

	up_array = np.hstack((u_l_array, u_r_array))
	down_array = np.hstack((d_l_array, d_r_array))
	E_array = np.vstack((up_array, down_array))
	print E_array, "E_array is get!"
	return E_array

def drawPicture(rating_array, result, color=True):
	'''
	绘制结果矩阵散点图
	'''
	userNum, itemNum = rating_array.shape
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
	mark = ['red', 'green', 'blue', 'black', 'pink']
	x = 0
	markIndex = 0
	for key1 in user_result.keys():
		for item1 in user_result[key1]:
			x += 1
			itemValues = rating_array[item1]
			y = 0
			for key2 in item_result.keys():
				for item2 in item_result[key2]:
					y += 1
					if int(itemValues[item2])!=0:
						if color:
							plt.scatter(x, y, marker = '.', s = 5, color = mark[markIndex])
							#plt.plot(x, y, mark[markIndex])
						else:
							plt.scatter(x, y, marker = '.', s = 5)
							#plt.plot(x, y, 'or')
		markIndex += 1
	plt.show()

def main():
	userid_dict = key2value(ratings, "userId")	#userid映射

	movieDict = movieCount(ratings, "movieId")	#统计电影被评分次数
	numLimit = len(userid_dict)*0.2	#定义热门电影的观看次数（即多少人观看过的电影算是热门电影）
	hotMovieList = findHotMovie(movieDict, numLimit)	#找出评分次数多的热门电影

	movieid_dict = key2value(ratings, "movieId", hotMovieList)	#movieid映射
	value_ratings = ratings.values[ : , 0:3]

	rating_array = getRatingarray(value_ratings, movieid_dict, userid_dict)
	E_array = getEarray(rating_array, movieid_dict, userid_dict)
	print E_array.shape
	Lbar = spe.getNormLaplacian(E_array)
	print Lbar
	k = 4
	kEigVal,kEigVec=spe.getKSmallestEigVec(Lbar,k)
	nodeNum = len(kEigVal)
	print "kEigVec = ", kEigVec

	'''
	#利用自带的k-means算法完成分类（可以进行多维分类）
	whitened = scv.whiten(kEigVec)
	center = scv.kmeans(whitened, k)[0]		#这里k取值不一定要等于获取的最小特征值个数k
	res = scv.vq(whitened, center)
	result = res[0]
	'''
	#利用自带的层次聚类算法完成分类
	d = sch.distance.pdist(kEigVec)
	Z = sch.linkage(d, method = 'complete')
	p = 0.5
	result = sch.fcluster(Z, p*d.max(), 'distance')

	#画出聚类前矩阵图与聚类后矩阵图
	userNum, itemNum = rating_array.shape
	temp = [i for i in xrange(userNum)] + [j for j in xrange(itemNum)]
	init_result = np.array(temp)
	#drawPicture(rating_array, init_result, False)
	drawPicture(rating_array, result)
	
if __name__ == '__main__':
	start = datetime.datetime.now()
	main()
	end = datetime.datetime.now()
	print "Running time: ", (end-start).seconds