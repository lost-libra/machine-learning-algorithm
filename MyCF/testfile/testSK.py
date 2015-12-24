#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os
from sklearn.cluster.bicluster import SpectralBiclustering
from sklearn.cluster import spectral_clustering
import testCF as cf
import testDP as dp
import testClustering as cs

def main():
	src_path = os.path.join(os.getcwd(), 'ratings.csv')
	res_path = os.path.join(os.getcwd(), 'preRatings.csv')
	predicted_data = pd.read_csv(res_path, header = 0, index_col = 0)
	int_col = []
	for col in predicted_data.columns:
		icol = int(col)
		int_col.append(icol)
	predicted_data.columns = int_col
	movie_rated_num = pd.Series(index = predicted_data.columns)
	for i in predicted_data.columns.values:
		movie_rated_num[i] = predicted_data[i].dropna().count()
	movie_rated_num.sort()
	cuted_data = predicted_data.loc[ : , movie_rated_num[8500: ].index]
	print cuted_data.shape

	data_matrix = cuted_data.fillna(0).values

	for i in range(0, len(data_matrix)):
		for j in range(0, len(data_matrix[i])):
			if data_matrix[i][j]>3.5:
				data_matrix[i][j] = 2
			elif data_matrix[i][j]<2.5:
				data_matrix[i][j] = 0
			else:
				data_matrix[i][j] = 1
	print data_matrix

	E_matrix = cs.getEMatrix(data_matrix)

	labels = spectral_clustering(E_matrix, n_clusters = 20)
	print labels
	'''
	init_data = pd.read_csv(src_path, header = 0, index_col = 0)
	# Cause the type of columns that read in csv is str, we need to convert it into int
	int_col = [int(col) for col in init_data.columns]
	init_data.columns = int_col
	init_data = init_data.loc[predicted_data.index, predicted_data.columns]
	init_data_matrix = init_data.fillna(0).values
	'''
	columns = ['userID', 'movieID', 'rating', 'timestamp']
	ratings = pd.read_csv(src_path, header = 1, names = columns)
	data = ratings.pivot(index = 'userID', columns = 'movieID', values = 'rating')
	init_data = data.loc[cuted_data.index, cuted_data.columns]
	init_data_matrix = init_data.fillna(0).values
	dp.drawPicture(init_data_matrix, labels)

	'''
	sbc = SpectralBiclustering(n_clusters = 2)
	sbc.fit(data_matrix)
	for i in range(0, 4):
		print sbc.get_indices(i)
	'''

if __name__ == '__main__':
	main()