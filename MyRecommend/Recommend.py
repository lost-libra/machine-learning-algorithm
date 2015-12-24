#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os

def number2coefficient(user_genres_data):
	'''Based on user_genres_data, find each genre's coefficient:
		coefficient = genre_number / total_genre_number

		Return user_genres_coe(type is DataFrame)
	'''
	user_genres_coe = pd.DataFrame(index = user_genres_data.index, columns = user_genres_data.columns)
	user_genres_coe.fillna(0)
	for user_id in user_genres_data.index:
		rating_num = user_genres_data.loc[user_id].sum()
		user_genres_coe.loc[user_id] = user_genres_data.loc[user_id]/rating_num
	return user_genres_coe

def average_rating(rating_data, min_num):
	'''Find movies' average rating and its rating number
		The parameter min_num is the threshold of minimum rating number of movie

		Return movie_aver_rating(type is DataFrame)
	'''
	user_movie_data = rating_data.pivot(index = 'userid', columns = 'movieid', values = 'rating')
	columns = ['averating', 'number']
	movie_aver_rating = pd.DataFrame(index = user_movie_data.columns, columns = columns)
	movie_aver_rating['averating'] = user_movie_data.mean()
	movie_aver_rating['number'] = user_movie_data.notnull().sum()
	movie_aver_rating = movie_aver_rating[movie_aver_rating['number']>min_num]
	return movie_aver_rating

def genres_movie(movie_genres_data, movie_aver_rating):
	'''Create a dict which keys are genres and values are movieids

		Return genres_movie_dict(type is dict)
	'''
	genres_movie_dict = {}
	useful_movieid = movie_aver_rating.index.values
	for movieid, title, genre in movie_genres_data.itertuples():
		if movieid in useful_movieid:
			this_genre = genre.split('|')
			for g in this_genre:
				if genres_movie_dict.has_key(g):
					genres_movie_dict[g].append(movieid)
				else:
					genres_movie_dict[g] = [movieid]
	for genre in genres_movie_dict.keys():
		genres_movie_dict[genre] = movie_aver_rating['averating'].loc[genres_movie_dict[genre]].order(ascending = False).index.values
	return genres_movie_dict

def recommend(user_genres_coe, movie_aver_rating, genres_movie_dict, lucky_users):
	'''We choice lucky_users as our target to recommend them movies of the genres that they love

	'''
	for user in lucky_users:
		love_genres =  user_genres_coe.loc[user].order(ascending = False)[ : 5].index.values
		print love_genres
		for love_genre in love_genres:
			print genres_movie_dict[love_genre][ : 5]

def main():
	local_path = os.getcwd()
	#Rating data [userid, movieid, rating]
	rating_src_path = os.path.join(local_path, 'src/ratings.csv')
	columns = ['userid', 'movieid', 'rating', 'timestamp']
	rating_data = pd.read_csv(rating_src_path, header = 0, names = columns)
	#User genres data [userid, [genre 1, ..., genre n]]
	user_genres_src_path = os.path.join(local_path, 'src/user_genres_data.csv')
	user_genres_data = pd.read_csv(user_genres_src_path, header = 0, index_col = 0)
	#Movie data [movieid, title, genre]
	movie_src_path = os.path.join(local_path, 'src/movies.csv')
	columns = ['titles', 'genres']
	movie_genres_data = pd.read_csv(movie_src_path, header = 0, index_col = 0, encoding = 'gbk', names = columns)
	#Compute user genre coefficient, which represent the love level of each user to each genre
	user_genres_coe = number2coefficient(user_genres_data)
	#Compute each movie's average rating and ignore movie which doesn't have min_num ratings
	min_num = 9
	movie_aver_rating = average_rating(rating_data, min_num)
	#Find genres movie dict, keys are genres, values are movies
	genres_movie_dict = genres_movie(movie_genres_data, movie_aver_rating)
	lucky_users = [1, 2, 3]
	recommend(user_genres_coe, movie_aver_rating, genres_movie_dict, lucky_users)

if __name__ == '__main__':
	main()