#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.cluster import Ward
from sklearn.cluster.bicluster import SpectralBiclustering
from sklearn.cluster import spectral_clustering

import pyfile.evaluate_cf as ecf

def LoadData():
	print 'loading data......'
	local_path = os.getcwd()

	ug_src_path = os.path.join(local_path, 'ml-1m/user_genres_data.csv')
	user_genres_data = pd.read_csv(ug_src_path, header = 0, index_col = 0)

	movie_src_path = 'ml-1m/movies.dat'
	columns_1 = ['movieid', 'titles', 'genres']
	movie_genres_data = pd.read_table(movie_src_path, sep = '::', header = None, index_col = 0, encoding = 'gbk', names = columns_1)

	predictedrating_src_path = os.path.join(local_path, 'ml-1m/predictedratings.dat')
	predictedratings = pd.read_table(predictedrating_src_path, sep = ',', header = 0, index_col = 0)
	predictedratings.columns = [int(x) for x in predictedratings.columns]

	rating_src_path = os.path.join(local_path, 'ml-1m/smallratings.dat')
	ratings = pd.read_table(rating_src_path, sep = ',', header = 0, index_col = 0)
	int_col = [int(x) for x in ratings.columns]
	ratings.columns = int_col
	return ratings, predictedratings, user_genres_data, movie_genres_data

def movie_genres(movie_genres_data):
	'''Create a dict which keys are movieids and values are movie genres

		Return movie_genre_dict(type is dict) and genre(type is set)
	'''
	movie_genre_dict = {}
	genres = set()
	for movieid, title, genre in movie_genres_data.itertuples():
		this_genre = genre.split('|')
		movie_genre_dict[movieid] = this_genre
		genres = genres | set(this_genre)
	return movie_genre_dict, genres

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

def EvaCF(ratings, result, n):
	print 'evaluating......'
	evaluate_results = pd.DataFrame()
	evaluate_time = n
	for i in range(evaluate_time):
		evaluate_result = pd.Series()
		userid = ratings.index.values
		part = 0
		for cls in set(result):
			part += 1
			cls_index = [userid[x] for x in range(len(userid)) if result[x]==cls]
			cls_rating_data = ratings.loc[cls_index]
			print ('The %d part in the %dth evaluate')%(part, i+1)
			cls_evaluate_result = ecf.evaluateCF(cls_rating_data, 50)
			evaluate_result = evaluate_result.append(cls_evaluate_result)
		evaluate_results[i] = evaluate_result
	print evaluate_results.describe()
	print 'Total : ', evaluate_results.mean().describe()

def EvaClu(ratings, result, user_genres_data, movie_genres_data, top_n = 5):
	print 'evaluate cluster result......'
	#由于电影本身种类是不均衡的，故引入movie_genres_col参数
	#该参数是每个电影种类占总种类的百分比
	movie_genre_dict, genres = movie_genres(movie_genres_data)
	genres_num = pd.Series(index = list(genres), data = [0]*len(genres))
	for movie in movie_genre_dict.keys():
		for genre in movie_genre_dict[movie]:
			genres_num[genre] += 1
	movie_genres_col = genres_num/genres_num.sum()

	userid = ratings.index.values
	genres = user_genres_data.columns
	class_genres_data = pd.DataFrame(index = set(result), columns = genres)
	class_genres_data = class_genres_data.fillna(0)
	n = top_n
	for user_index in range(len(result)):
		user_id = userid[user_index]
		user_class = result[user_index]
		#根据movie_genres_col参数 均衡电影种类个数
		balance_user_data = user_genres_data.loc[user_id]/movie_genres_col
		faver_sort = balance_user_data.order(ascending = False)
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
	print 'Done.'

def main():
	#Step 1 : Load data
	ratings, predictedratings, user_genres_data, movie_genres_data = LoadData()
	rating_data = ratings.fillna(0)
	predictedrating_data = predictedratings.fillna(0)
	genres = user_genres_data.columns.values
	user_genres_col = user_genres_data.copy()
	for user in user_genres_data.index:
		total = user_genres_data.loc[user].sum()
		user_genres_col.loc[user] = user_genres_data.loc[user]/total
	'''
	#delete hot topic
	hot_topic = user_genres_col.sum().order(ascending = False)[:2].index.values
	user_genres_col = user_genres_col.drop(hot_topic, axis = 1)
	'''

	#Step 2 : Choice one data set and do some operate to cluster
	#we need to ignore hot movies to improve the clusters' accuracy
	user_num = len(ratings.index)
	t = user_num / 3
	target_movie = ratings.count()[ratings.count()<t].index

	#using_data is the data set that we use to do cluster
	using_data = rating_data[target_movie].copy()
	#using_data = user_genres_col.copy()

	#Step 3 : Choice one cluster algorithm to do cluster
	print 'clustering......'
	#cluster
	data_matrix = using_data.values
	'''
	#use spectral clustering
	E_matrix = eclu.getEMatrix(data_matrix)
	result_total = spectral_clustering(E_matrix, n_clusters = 8)
	result = result_total[ : len(ratings.values)]
	#use k-means
	km = KMeans(n_clusters = 5)
	km.fit(data_matrix)
	result = km.predict(data_matrix)
	'''
	#use Hierarchical clustering
	ac = Ward(n_clusters=5)
	ac.fit(data_matrix)
	result = ac.fit_predict(data_matrix)
	
	print 'cluster result = ', result
	print 'cluster number = ', len(set(result))

	#Step 4 : Evaluate result
	#EvaCF(ratings, result, 10)
	EvaClu(ratings, result, user_genres_data, movie_genres_data, top_n = 5)

if __name__ == '__main__':
	main()