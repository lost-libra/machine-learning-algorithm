#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os
from sklearn.cluster.bicluster import SpectralBiclustering
from sklearn.cluster import spectral_clustering
from sklearn.cluster import KMeans

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

	top_matrix = np.hstack((t_l_matrix, t_r_matrix))
	bottom_matrix = np.hstack((b_l_matrix, b_r_matrix))
	E_matrix = np.vstack((top_matrix, bottom_matrix))
	return E_matrix
	
def evaluateSC(rating_data):
	return 0

def main():
	local_path = os.getcwd()
	ug_src_path = os.path.join(local_path, 'ml-1m/user_genres_data.csv')
	user_genres_data = pd.read_csv(ug_src_path, header = 0, index_col = 0)
	genres = user_genres_data.columns.values

	rating_src_path = os.path.join(local_path, 'ml-1m/smallratings.dat')
	rating_data = pd.read_table(rating_src_path, sep = ',', header = 0, index_col = 0)
	int_col = [int(x) for x in rating_data.columns]
	rating_data.columns = int_col
	rating_data = rating_data.fillna(0)

	predictedrating_src_path = os.path.join(local_path, 'ml-1m/predictedratings.dat')
	predictedratings = pd.read_table(predictedrating_src_path, sep = ',', header = 0, index_col = 0)
	predictedratings.columns = [int(x) for x in predictedratings.columns]
	predictedrating_data = predictedratings.fillna(0)

	userid = predictedrating_data.index.values
	km = KMeans(n_clusters = 8)
	km.fit(predictedrating_data.values)
	result = km.predict(predictedrating_data.values)
	print result
	class_genres_data = pd.DataFrame(index = set(result), columns = genres)
	class_genres_data = class_genres_data.fillna(0)
	n = 5
	for user_index in range(len(result)):
		user_id = userid[user_index]
		user_class = result[user_index]
		faver_sort = user_genres_data.loc[user_id].order(ascending = False)
		score = n
		for genre in faver_sort.index.values[ : n]:
			score -= 1
			class_genres_data.loc[user_class, genre] += score
	print class_genres_data
	class_genres_co = class_genres_data.copy()
	for class_id in class_genres_data.index:
		score = class_genres_data.loc[class_id].sum()
		class_genres_co.loc[class_id] = (class_genres_data.loc[class_id]/score) * 100
	print class_genres_co



if __name__ == '__main__':
	main()