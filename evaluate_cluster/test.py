#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os
from sklearn.cluster import KMeans
import pyfile.MovieGenres as MG

def main():
	user_genres_path = 'ml-1m/user_genres_data.csv'
	user_genres_data = pd.read_csv(user_genres_path, header = 0, index_col = 0)
	rating_path = 'ml-1m/smallratings.dat'
	ratings = pd.read_table(rating_path, sep = ',', header = 0, index_col = 0)
	movie_src_path = 'ml-1m/movies.dat'
	columns_1 = ['movieid', 'titles', 'genres']
	movie_genres_data = pd.read_table(movie_src_path, sep = '::', header = None, index_col = 0, encoding = 'gbk', names = columns_1)

	movie_genre_dict, genres = MG.movie_genres(movie_genres_data)

	genres_num = pd.Series(index = list(genres), data = [0]*len(genres))
	for movie in movie_genre_dict.keys():
		for genre in movie_genre_dict[movie]:
			genres_num[genre] += 1
	print genres_num
	movie_genres_col = genres_num/genres_num.sum()
	print movie_genres_col

if __name__ == '__main__':
	main()