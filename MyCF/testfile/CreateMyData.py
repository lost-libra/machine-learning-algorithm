#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd

def main():
	movies = [m for m in range(1, 151)]
	users = [u for u in range(1, 101)]
	myData = pd.DataFrame(index = users, columns = movies, dtype = int)
	#print myData[:10]

	rand_movie = np.random.permutation(movies)		#permutation will randomly resort array
	movie_class1 = rand_movie[ : 55]
	movie_class2 = rand_movie[40 : 110]
	movie_class3 = rand_movie[100 : ]
	movie_map = [movie_class1]+[movie_class2]+[movie_class3]
	rand_user = np.random.permutation(users)
	user_class1 = rand_user[ : 40]
	user_class2 = rand_user[40 : 65]
	user_class3 = rand_user[65 : ]
	user_map = [user_class1]+[user_class2]+[user_class3]
	print movie_map
	print user_map
	print np.random.randint(0,2)
	uclass_index = 0
	for user_class in user_map:
		uclass_index += 1
		for user in user_class:
			mclass_index = 0
			for movie_class in movie_map:
				mclass_index += 1
				for movie in movie_class:
					if uclass_index==mclass_index:
						if np.random.randint(0, 2)==0:
							myData.loc[user, movie] = np.random.randint(4, 6)
					else:
						if np.random.randint(0, 4)==0:
							myData.loc[user, movie] = np.random.randint(1, 4)
	print myData
	myData.to_csv('datatestcv_3.csv')


if __name__ == '__main__':
	main()