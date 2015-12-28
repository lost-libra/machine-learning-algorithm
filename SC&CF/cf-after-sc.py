#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.cluster.bicluster import SpectralBiclustering
from sklearn.cluster import spectral_clustering
import evaluate_cf as ec
import evaluate_sc as es

def main():
	print 'loading data......'
	local_path = os.getcwd()
	#three ways to cluster users
	#First, we can use genres that users most rated to cluster
	ug_src_path = os.path.join(local_path, 'ml-1m/user_genres_data.csv')
	user_genres_data = pd.read_csv(ug_src_path, header = 0, index_col = 0)
	genres = user_genres_data.columns.values
	user_genres_col = user_genres_data.copy()
	for user in user_genres_data.index:
		total = user_genres_data.loc[user].sum()
		user_genres_col.loc[user] = user_genres_data.loc[user]/total

	#We also can use predicted rating to cluster
	predictedrating_src_path = os.path.join(local_path, 'ml-1m/predictedratings.dat')
	predictedratings = pd.read_table(predictedrating_src_path, sep = ',', header = 0, index_col = 0)
	predictedratings.columns = [int(x) for x in predictedratings.columns]
	predictedrating_data = predictedratings.fillna(0)

	#We also can use predicted rating to cluster
	rating_src_path = os.path.join(local_path, 'ml-1m/smallratings.dat')
	ratings = pd.read_table(rating_src_path, sep = ',', header = 0, index_col = 0)
	int_col = [int(x) for x in ratings.columns]
	ratings.columns = int_col
	rating_data = ratings.fillna(0)

	print 'clustering......'
	#use predicted data to cluster
	data_matrix = predictedrating_data.values

	'''
	#use spectral clustering
	E_matrix = es.getEMatrix(data_matrix)
	result_total = spectral_clustering(E_matrix, n_clusters = 8)
	result = result_total[ : len(ratings.values)]
	'''
	#use k-means
	km = KMeans(n_clusters = 8)
	km.fit(data_matrix)
	result = km.predict(data_matrix)

	print 'cluster result = ', result

	print 'evaluating......'
	#use init data to evaluate
	evaluate_result = pd.Series()
	userid = ratings.index.values
	for cls in set(result):
		cls_index = [userid[x] for x in range(len(userid)) if result[x]==cls]
		cls_rating_data = ratings.loc[cls_index]
		cls_evaluate_result = ec.evaluateCF(cls_rating_data)
		evaluate_result = evaluate_result.append(cls_evaluate_result)
	print evaluate_result.describe()
	print 'mean:   ', evaluate_result.mean()
	print 'std:    ', evaluate_result.std()


if __name__ == '__main__':
	main()