#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import scipy as sp
import scipy.cluster.vq as scv
import scipy.cluster.hierarchy as sch
import os

import testCF as cf
import testDP as dp

def getNormLaplacian(W):
	"""input matrix W=(w_ij)
	"compute D=diag(d1,...dn)
	"and L=D-W
	"and Lbar=D^(-1/2)LD^(-1/2)
	"return Lbar
	"""
	d=[np.sum(row) for row in W]
	D=np.diag(d)
	L=D-W
	# Dn=D^(-1/2)
	Dn=np.power(np.linalg.matrix_power(D,-1),0.5)
	Lbar=np.dot(np.dot(Dn,L),Dn)
	return Lbar

def getKSmallestEigVec(Lbar,k):
	"""input
	"matrix Lbar and k
	"return
	"k smallest eigen values and their corresponding eigen vectors
	"""
	eigval,eigvec=np.linalg.eig(Lbar)
	dim=len(eigval)

	# Find the smallest k eigval
	dictEigval=dict(zip(eigval,range(0,dim)))
	kEig=np.sort(eigval)[0:k]
	ix=[dictEigval[k] for k in kEig]
	return eigval[ix],eigvec[:,ix]

def getEMatrix(data_matrix):
	'''构建二部图邻接矩阵E
	'E = [[0 A],
	'	[transpose(A) 0]],
	'其中A为二部图的N×M矩阵，N为总user数量，M为总电影数量
	'''
	userNum, movieNum = data_matrix.shape
	t_l_matrix = np.zeros((userNum, userNum))
	t_r_matrix = data_matrix
	b_l_matrix = data_matrix.transpose()
	b_r_matrix = np.zeros((movieNum, movieNum))
	print t_l_matrix.shape, t_r_matrix.shape, b_l_matrix.shape, b_r_matrix.shape

	top_matrix = np.hstack((t_l_matrix, t_r_matrix))
	bottom_matrix = np.hstack((b_l_matrix, b_r_matrix))
	E_matrix = np.vstack((top_matrix, bottom_matrix))
	print 'E_matrix = \n', E_matrix
	return E_matrix

def SpectralClustering(data_matrix, k):
	E_matrix = getEMatrix(data_matrix)
	print E_matrix.shape

	Lbar = getNormLaplacian(E_matrix)
	kEigVal,kEigVec=getKSmallestEigVec(Lbar,k)
	nodeNum = len(kEigVal)

	# 利用自带的k-means算法完成分类（可以进行多维分类）
	whitened = scv.whiten(kEigVec)
	center = scv.kmeans(whitened, k)[0]		#这里k取值不一定要等于获取的最小特征值个数k
	res = scv.vq(whitened, center)
	return res

def main():
	# Use predicted data to do clustering
	# Predicted_data = cf.CollaborativeFiltering(srcPath)
	src_path = os.path.join(os.getcwd(), 'datatestcv_3.csv')
	res_path = os.path.join(os.getcwd(), 'pretestDatacv_3.csv')
	predicted_data = pd.read_csv(res_path, header = 0, index_col = 0)

	# Cause the type of columns that read in csv is str, we need to convert it into int
	int_col = []
	for col in predicted_data.columns:
		icol = int(col)
		int_col.append(icol)
	predicted_data.columns = int_col
	
	data_matrix = predicted_data.fillna(0).values
	print data_matrix

	# Change the data_matrix, we define that if user love this movie, he will rate this movie more than 3.5;
	# If user doesn't love this movie, he will rate this movie less than 2.5; 
	# If user rates one movie 3, we define he think this movie is normal.
	for i in range(0, len(data_matrix)):
		for j in range(0, len(data_matrix[i])):
			if data_matrix[i][j]>3.5:
				data_matrix[i][j] = 2
			elif data_matrix[i][j]<2.5:
				data_matrix[i][j] = 0
			else:
				data_matrix[i][j] = 1
	print data_matrix

	res = SpectralClustering(data_matrix, 6)
	result = res[0]
	print result[:100]
	print result[100:]

	init_data = pd.read_csv(src_path, header = 0, index_col = 0)
	# Cause the type of columns that read in csv is str, we need to convert it into int
	int_col = [int(col) for col in init_data.columns]
	init_data.columns = int_col
	init_data = init_data.loc[predicted_data.index, predicted_data.columns]
	init_data_matrix = init_data.fillna(0).values
	dp.drawPicture(init_data_matrix, result)

if __name__ == '__main__':
		main()