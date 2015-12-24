#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os

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

def user_genres(rating_data, movie_genre_dict, genres):
	'''Create a DataFrame which:
		index are userids,
		columns are genres,
		values are numbers of genres that user has rated

		Return user_genres_data(type is DataFrame)
	'''
	user_id = rating_data.userid.unique()
	user_genres_data = pd.DataFrame(index = user_id, columns = genres)
	user_genres_data = user_genres_data.fillna(0)
	for index, userid, movieid, rating in rating_data.loc[ : , columns[:3]].itertuples():
		for genre in movie_genre_dict[movieid]:
			user_genres_data.loc[userid, genre] += 1
	user_genres_data.to_csv('src/user_genres_data.csv')
	return user_genres_data

def main():
	local_path = os.getcwd()
	movie_src_path = os.path.join(local_path, 'src/movies.csv')
	columns = ['titles', 'genres']
	movie_genres_data = pd.read_csv(movie_src_path, header = 0, index_col = 0, encoding = 'gbk', names = columns)
	rating_src_path = os.path.join(local_path, 'src/ratings.csv')
	columns = ['userid', 'movieid', 'rating', 'timestamp']
	rating_data = pd.read_csv(rating_src_path, header = 0, names = columns)

	#movie_genre_dict, genres = movie_genres(movie_genres_data)
	#user_genres_data = user_genres(rating_data, movie_genre_dict, genres)
	average_rating(rating_data)

if __name__ == '__main__':
	main()